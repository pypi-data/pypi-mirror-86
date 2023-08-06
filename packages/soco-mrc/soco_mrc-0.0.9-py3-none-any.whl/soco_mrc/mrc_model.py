from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from soco_mrc.cloud_bucket import CloudBucket
import numpy as np
import os
import torch
import re
from collections import namedtuple, defaultdict
from soco_mrc import util
from soco_mrc.model.bert_model import BertForMrcCls, BertForMrcClsFact, BertForMrcMultiSpanBio
from soco_device import DeviceCheck
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("transformers").setLevel(logging.ERROR)

MODEL_MAP = {
    'MrcModel': AutoModelForQuestionAnswering, 
    'MrcClsModel': BertForMrcCls, 
    'MrcClsMultiSpanModel': BertForMrcCls,
    'MrcClsFactModel': BertForMrcClsFact,
    'MrcMultiSpanBioModel': BertForMrcMultiSpanBio,
    }

class ModelBase(object):
    def __init__(self,
        region, 
        n_gpu=0,
        fp16=False, 
        quantize=False, 
        multiprocess=False
    ):
        logger.info("Op in {} region".format(region))
        self.n_gpu_request = n_gpu
        self.region = region
        self.fp16 = fp16
        self.quantize = quantize
        self.multiprocess = multiprocess
        self.cloud_bucket = CloudBucket(region)
        self._models = dict()
        self.max_input_length = 512
        self.device_check = DeviceCheck()


    def _load_model(self, model_id):
        # a naive check. if too big, just reset
        if len(self._models) > 20:
            self._models = dict()

        if model_id not in self._models:
            path = os.path.join('resources', model_id)
            self.cloud_bucket.download_model('mrc-models', model_id)
            model_class = self.__class__.__name__
            logger.info('class: {}'.format(model_class))
            model = MODEL_MAP[model_class].from_pretrained(path)
            tokenizer = AutoTokenizer.from_pretrained(path, use_fast=True)

            device_name, device_ids = self.device_check.get_device_by_model(model_id, n_gpu=self.n_gpu_request)
            self.n_gpu_allocate = len(device_ids)
            device = '{}:{}'.format(device_name, device_ids[0]) if self.n_gpu_allocate == 1 else device_name
            
            logger.info('device: {}'.format(device))

            if self.fp16 and 'cuda' in device:
                logger.info('Use fp16')
                model.half()
            if self.quantize and device == 'cpu':
                logger.info('Use quantization')
                model = torch.quantization.quantize_dynamic(
                    model, {torch.nn.Linear}, dtype=torch.qint8)
            model.to(device)

            # multi gpu inference
            if self.n_gpu_allocate > 1 and not isinstance(model, torch.nn.DataParallel):
                model = torch.nn.DataParallel(model, device_ids=device_ids)

            self._models[model_id] = (tokenizer, model, device)

        else:
            # if loaded as cpu, check if gpu is available
            _, _, device = self._models[model_id]
            if self.n_gpu_request > 0 and device == 'cpu':
                device_name, device_ids = self.device_check.get_device_by_model(model_id, n_gpu=1)
                new_device = '{}:{}'.format(device_name, device_ids[0]) if len(device_ids) == 1 else device_name
                if new_device != device:
                    logger.info('Reloading')
                    self._models.pop(model_id)
                    self._load_model(model_id)

        return self._models[model_id]


    def batch_predict(self, model_id, data, **kwargs):
        raise NotImplementedError

    def _get_param(self, kwargs):
        batch_size = kwargs.pop('batch_size', 10)
        merge_pred = kwargs.pop('merge_pred', False)
        stride = kwargs.pop('stride', 0)

        return batch_size, merge_pred, stride



class MrcModel(ModelBase):
    def batch_predict(self, model_id, data, **kwargs):
        batch_size, merge_pred, stride = self._get_param(kwargs)

        tokenizer, model, device = self._load_model(model_id)

        features = util.convert_examples_to_features(
                                                tokenizer, 
                                                data, 
                                                self.max_input_length,
                                                merge_pred,
                                                stride)

        results = []
        for batch in util.chunks(features, batch_size):
            padded = util.pad_batch(batch)
            input_ids, token_type_ids, attn_masks = padded

            with torch.no_grad():
                start_scores, end_scores = model(torch.tensor(input_ids).to(device),
                                                 token_type_ids=torch.tensor(token_type_ids).to(device),
                                                 attention_mask=torch.tensor(attn_masks).to(device))
                start_probs = torch.softmax(start_scores, dim=1)
                end_probs = torch.softmax(end_scores, dim=1)

            for b_id in range(len(batch)):
                all_tokens = tokenizer.convert_ids_to_tokens(input_ids[b_id])
                legal_length = batch[b_id]['length']
                b_start_score = start_scores[b_id][0:legal_length]
                b_end_score = end_scores[b_id][0:legal_length]
                token2char = batch[b_id]['offset_mapping']
                for t_id in range(legal_length):
                    if token2char[t_id] is None or token2char[t_id] == (0, 0):
                        b_start_score[t_id] = -10000
                        b_end_score[t_id] = -10000

                _, top_start_id = torch.topk(b_start_score, 2, dim=0)
                _, top_end_id = torch.topk(b_end_score, 2, dim=0)

                s_prob = start_probs[b_id, top_start_id[0]].item()
                e_prob = end_probs[b_id, top_end_id[0]].item()
                s_logit = start_scores[b_id, top_start_id[0]].item()
                e_logit = end_scores[b_id, top_end_id[0]].item()

                prob = (s_prob + e_prob) / 2
                score = (s_logit + e_logit) / 2

                doc = batch[b_id]['doc']
                doc_offset = input_ids[b_id].index(102)

                res = all_tokens[top_start_id[0]:top_end_id[0] + 1]
                char_offset = token2char[doc_offset + 1][0]
                example_idx = batch[b_id]['example_idx']

                if not res or res[0] == "[CLS]" or res[0] == '[SEP]' or top_start_id[0].item() <= doc_offset:
                    prediction = {'missing_warning': True,
                                  'prob': prob,
                                  'start_end_prob': [s_prob, e_prob],
                                  'score': score,
                                  'start_end_score': [s_logit, e_logit],
                                  'value': "", 
                                  'answer_start': -1,
                                  'example_idx': example_idx}
                else:
                    if not merge_pred:
                        start_map = token2char[top_start_id[0].item()]
                        end_map = token2char[top_end_id[0].item()]
                        span = [start_map[0] - char_offset, end_map[1] - char_offset]
                        ans = doc[span[0]: span[1]]
                    else:
                        base_idx = batch[b_id]['base_idx']
                        orig_doc = batch[b_id]['orig_doc']
                        orig_token2char = batch[b_id]['orig_offset_mapping']

                        # map token index, then use offset mapping to map to original position
                        orig_start_map = orig_token2char[top_start_id[0].item() + base_idx - doc_offset - 1]
                        orig_end_map = orig_token2char[top_end_id[0].item() + base_idx - doc_offset - 1]
                        span = [orig_start_map[0], orig_end_map[1]]
                        ans = orig_doc[span[0]: span[1]]
                        try:
                            start_map = token2char[top_start_id[0].item()]
                            end_map = token2char[top_end_id[0].item()]
                            debug_span = [start_map[0] - char_offset, end_map[1] - char_offset]
                            debug_ans = doc[debug_span[0]: debug_span[1]]
                            assert debug_ans == ans
                        except Exception as e:
                            print(e)
                            print('chunk ans: {} '.format(debug_ans))
                            print('doc ans: {} '.format(ans))
                            print('chunk span: {} vs doc span: {}'.format(debug_span, span))

                    prediction = {'value': ans,
                                  'answer_start': span[0],
                                  'answer_span': span,
                                  'prob': prob,
                                  'start_end_prob': [s_prob, e_prob],
                                  'score': score,
                                  'start_end_score': [s_logit, e_logit],
                                  'tokens': res,
                                  'example_idx': example_idx}

                results.append(prediction)

        # merge predictions
        if merge_pred:
            results = util.merge_predictions(results)

        return results


class MrcClsModel(ModelBase):
    def batch_predict(self, model_id, data, **kwargs):
        batch_size, merge_pred, stride = self._get_param(kwargs)
        ans_type = kwargs.get('ans_type', 'auto')

        tokenizer, model, device = self._load_model(model_id)
        
        features = util.convert_examples_to_features(
                                                tokenizer, 
                                                data, 
                                                self.max_input_length,
                                                merge_pred,
                                                stride)

        results = []
        for batch in util.chunks(features, batch_size):
            padded = util.pad_batch(batch)
            input_ids, token_type_ids, attn_masks = padded

            with torch.no_grad():
                start_scores, end_scores, target_scores = model(torch.tensor(input_ids).to(device),
                                                 token_type_ids=torch.tensor(token_type_ids).to(device),
                                                 attention_mask=torch.tensor(attn_masks).to(device))
                start_probs = torch.softmax(start_scores, dim=1)
                end_probs = torch.softmax(end_scores, dim=1)
                target_probs = torch.softmax(target_scores, dim=1)


            for b_id in range(len(batch)):
                all_tokens = tokenizer.convert_ids_to_tokens(input_ids[b_id])
                legal_length = batch[b_id]['length']
                b_start_score = start_scores[b_id][0:legal_length]
                b_end_score = end_scores[b_id][0:legal_length]
                token2char = batch[b_id]['offset_mapping']
                for t_id in range(legal_length):
                    # if token2char[t_id] is None or token2char[t_id] == (0, 0):
                    if token2char[t_id] is None:
                        b_start_score[t_id] = -10000
                        b_end_score[t_id] = -10000

                _, top_start_id = torch.topk(b_start_score, 2, dim=0)
                _, top_end_id = torch.topk(b_end_score, 2, dim=0)

                doc = batch[b_id]['doc']
                doc_offset = input_ids[b_id].index(102)

                res = all_tokens[top_start_id[0]:top_end_id[0] + 1]
                char_offset = token2char[doc_offset + 1][0]
                example_idx = batch[b_id]['example_idx']

                if not res or res[0] == "[CLS]" or res[0] == '[SEP]' or ans_type == 'yes_no':
                    # Here should handle three way cls (yes/no/noans)
                    # target_probs
                    no_ans_ind = int(torch.argmax(target_probs[b_id]).item())

                    final_text = ""

                    # if answer type is auto, we try to select.
                    if ans_type == "span":
                        final_text = ""  # UNKNOWN
                    else:
                        if no_ans_ind == 0:
                            final_text = ""  # UNKNOWN
                        elif no_ans_ind == 1:
                            final_text = "YES"
                        elif no_ans_ind == 2:
                            final_text = "NO"

                    prob = target_probs[b_id, no_ans_ind].item()
                    score = target_scores[b_id, no_ans_ind].item()
                    
                    prediction = {'value_type': 'classification',
                                  'prob': prob,
                                  'start_end_prob': [prob, prob],
                                  'score': score,
                                  'start_end_score': [score, score],
                                  'value': final_text,
                                  'answer_start': -1,
                                  'example_idx': example_idx}
                    if not final_text:
                        prediction['missing_warning'] = True
                else:

                    s_prob = start_probs[b_id, top_start_id[0]].item()
                    e_prob = end_probs[b_id, top_end_id[0]].item()
                    s_logit = start_scores[b_id, top_start_id[0]].item()
                    e_logit = end_scores[b_id, top_end_id[0]].item()

                    prob = (s_prob + e_prob) / 2
                    score = (s_logit + e_logit) / 2

                    if not merge_pred:
                        start_map = token2char[top_start_id[0].item()]
                        end_map = token2char[top_end_id[0].item()]
                        span = [start_map[0] - char_offset, end_map[1] - char_offset]
                        ans = doc[span[0]: span[1]]
                    else:
                        base_idx = batch[b_id]['base_idx']
                        orig_doc = batch[b_id]['orig_doc']
                        orig_token2char = batch[b_id]['orig_offset_mapping']

                        # map token index, then use offset mapping to map to original position
                        orig_start_map = orig_token2char[top_start_id[0].item() + base_idx - doc_offset - 1]
                        orig_end_map = orig_token2char[top_end_id[0].item() + base_idx - doc_offset - 1]
                        span = [orig_start_map[0], orig_end_map[1]]
                        ans = orig_doc[span[0]: span[1]]
                        try:
                            start_map = token2char[top_start_id[0].item()]
                            end_map = token2char[top_end_id[0].item()]
                            debug_span = [start_map[0] - char_offset, end_map[1] - char_offset]
                            debug_ans = doc[debug_span[0]: debug_span[1]]
                            assert debug_ans == ans
                        except Exception as e:
                            print(e)
                            print('chunk ans: {} '.format(debug_ans))
                            print('doc ans: {} '.format(ans))
                            print('chunk span: {} vs doc span: {}'.format(debug_span, span))

                    prediction = {'value': ans,
                                  'value_type': 'span',
                                  'answer_start': span[0],
                                  'answer_span': span,
                                  'prob': prob,
                                  'start_end_prob': [s_prob, e_prob],
                                  'score': score,
                                  'start_end_score': [s_logit, e_logit],
                                  'tokens': res,
                                  'example_idx': example_idx}

                results.append(prediction)

        # merge predictions
        if merge_pred:
            results = util.merge_predictions(results)

        return results


class MrcClsMultiSpanModel(ModelBase):
    def batch_predict(self, model_id, data, **kwargs):
        batch_size, merge_pred, stride = self._get_param(kwargs)
        if merge_pred:
            logger.warn('Merging prediction not implemented yet for {}'.format(self.__class__.__name__))

        n_best = kwargs.pop('n_best', 10)

        ans_type = kwargs.pop('ans_type', 'auto')
        prob_thresh = kwargs.pop('prob_thresh', None)
        use_heuristic = kwargs.pop('use_heuristic', False)
        filter_type = kwargs.pop('filter_type', 'subset')
        lang = kwargs.pop('lang', 'zh')

        tokenizer, model, device = self._load_model(model_id)

        features = util.convert_examples_to_features(tokenizer, data, self.max_input_length)

        results = []
        for batch in util.chunks(features, batch_size):
            padded = util.pad_batch(batch)
            input_ids, token_type_ids, attn_masks = padded

            with torch.no_grad():
                start_scores, end_scores, target_scores = model(torch.tensor(input_ids).to(device),
                                                 token_type_ids=torch.tensor(token_type_ids).to(device),
                                                 attention_mask=torch.tensor(attn_masks).to(device))
                start_probs = torch.softmax(start_scores, dim=1)
                end_probs = torch.softmax(end_scores, dim=1)
                target_probs = torch.softmax(target_scores, dim=1)


            for b_id in range(len(batch)):
                all_tokens = tokenizer.convert_ids_to_tokens(input_ids[b_id])
                legal_length = batch[b_id]['length']
                b_start_score = start_scores[b_id][0:legal_length]
                b_end_score = end_scores[b_id][0:legal_length]
                token2char = batch[b_id]['offset_mapping']
                for t_id in range(legal_length):
                    # if token2char[t_id] is None or token2char[t_id] == (0, 0):
                    if token2char[t_id] is None:
                        b_start_score[t_id] = -10000
                        b_end_score[t_id] = -10000

                _, top_start_id = torch.topk(b_start_score, n_best, dim=0)
                _, top_end_id = torch.topk(b_end_score, n_best, dim=0)

                doc = batch[b_id]['doc']
                doc_offset = input_ids[b_id].index(102)

                res = all_tokens[top_start_id[0]:top_end_id[0] + 1]
                char_offset = token2char[doc_offset + 1][0]

                if not res or res[0] == "[CLS]" or res[0] == '[SEP]' or ans_type == 'yes_no':
                    # Here should handle three way cls (yes/no/noans)
                    # target_probs
                    no_ans_ind = int(torch.argmax(target_probs[b_id]).item())

                    final_text = ""

                    # if answer type is auto, we try to select.
                    if ans_type == "span":
                        final_text = ""  # UNKNOWN
                    else:
                        if no_ans_ind == 0:
                            final_text = ""  # UNKNOWN
                        elif no_ans_ind == 1:
                            final_text = "YES"
                        elif no_ans_ind == 2:
                            final_text = "NO"

                    prob = target_probs[b_id, no_ans_ind].item()
                    score = target_scores[b_id, no_ans_ind].item()
                    
                    prediction = {'value_type': 'classification',
                                  'prob': prob,
                                  'start_end_prob': [prob, prob],
                                  'score': score,
                                  'start_end_score': [score, score],
                                  'value': final_text,
                                  'answer_start': -1}
                    if not final_text:
                        prediction['missing_warning'] = True
                else:
                    comparator = util.ZhAnswerComparator() if lang=='zh' else util.EnAnswerComparator()
                    records = []
                    record = namedtuple(
                        'prediction',
                        ['s_id', 'e_id', 's_prob', 'e_prob', 's_logit', 'e_logit'])

                    for s_id in top_start_id:
                        for e_id in top_end_id:
                            if e_id < s_id:
                                continue
                            if e_id == 0 or s_id == 0:
                                continue
                            if all_tokens[s_id] in ['[SEP]', '[CLS]'] or all_tokens[e_id] in ['[SEP]', '[CLS]']:
                                continue

                            s_prob = start_probs[b_id, s_id].item()
                            e_prob = end_probs[b_id, e_id].item()
                            s_logit = start_scores[b_id, s_id].item()
                            e_logit = end_scores[b_id, e_id].item()
                            if prob_thresh and (s_prob + e_prob) < prob_thresh:
                                continue

                            records.append(record(
                                s_id=s_id,
                                e_id=e_id,
                                s_prob=s_prob,
                                e_prob=e_prob,
                                s_logit = s_logit,
                                e_logit = e_logit))

                    # heuristic from https://arxiv.org/abs/1906.03820
                    if use_heuristic:
                        records = sorted(
                            records,
                            key=lambda x: (x.s_prob + x.e_prob - (x.e_id - x.s_id + 1)),
                            reverse=True)
                    else:
                        records = sorted(
                            records,
                            key=lambda x: (x.s_prob + x.e_prob),
                            reverse=True)

                    prediction = defaultdict(list)
                    for i, pred_i in enumerate(records):
                        if len(prediction['value']) >= int(n_best)/2:
                            break
                        start_map = token2char[pred_i.s_id]
                        end_map = token2char[pred_i.e_id]
                        span = [start_map[0] - char_offset, end_map[1] - char_offset]
                        ans = doc[span[0]: span[1]]
                        prob = (pred_i.s_prob + pred_i.e_prob) / 2
                        score = (pred_i.s_logit + pred_i.e_logit) / 2
                        res = all_tokens[pred_i.s_id:pred_i.e_id + 1]

                        prediction['value_type'] = 'multi_span'
                        prediction['value'].append(ans)
                        prediction['prob'].append(prob)
                        prediction['start_end_prob'].append([pred_i.s_prob, pred_i.e_prob])
                        prediction['score'].append(score)
                        prediction['start_end_score'].append([pred_i.s_logit, pred_i.e_logit])
                        prediction['answer_start'].append(span[0])
                        prediction['answer_span'].append(span)
                        prediction['tokens'].append(res)

                        if (i+1) < len(records):
                            indexes = []
                            for j, pred_j in enumerate(records[(i+1):]):
                                start_map_j = token2char[pred_j.s_id]
                                end_map_j = token2char[pred_j.e_id]
                                span_j = [start_map_j[0] - char_offset, end_map_j[1] - char_offset]
                                ans_j = doc[span_j[0]: span_j[1]]

                                if filter_type == 'f1':
                                    if comparator.compute_f1(ans, ans_j) > 0:
                                        indexes.append(i + j + 1)
                                elif filter_type == 'subset':
                                    if ans_j in ans or ans in ans_j:
                                        indexes.append(i + j + 1)
                                elif filter_type == 'index':    
                                    # check if span overlaps
                                    if span[0] <= span_j[1] and span_j[0] <= span[1]:
                                        indexes.append(i + j + 1)

                            [records.pop(index - k) for k, index in enumerate(indexes)]



                results.append(prediction)

        return results



class MrcClsFactModel(ModelBase):
    def batch_predict(self, model_id, data, **kwargs):
        batch_size, merge_pred, stride = self._get_param(kwargs)
        ans_type = kwargs.pop('ans_type', 'auto')

        tokenizer, model, device = self._load_model(model_id)

        features = util.convert_examples_to_features(
                                                tokenizer, 
                                                data, 
                                                self.max_input_length,
                                                merge_pred,
                                                stride)

        results = []
        for batch in util.chunks(features, batch_size):
            padded = util.pad_batch(batch)
            input_ids, token_type_ids, attn_masks = padded

            with torch.no_grad():
                start_scores, end_scores, target_scores = model(torch.tensor(input_ids).to(device),
                                                 token_type_ids=torch.tensor(token_type_ids).to(device),
                                                 attention_mask=torch.tensor(attn_masks).to(device))
                start_probs = torch.softmax(start_scores, dim=1)
                end_probs = torch.softmax(end_scores, dim=1)
                target_probs = torch.softmax(target_scores, dim=1)


            for b_id in range(len(batch)):
                all_tokens = tokenizer.convert_ids_to_tokens(input_ids[b_id])
                legal_length = batch[b_id]['length']
                b_start_score = start_scores[b_id][0:legal_length]
                b_end_score = end_scores[b_id][0:legal_length]
                token2char = batch[b_id]['offset_mapping']
                for t_id in range(legal_length):
                    # if token2char[t_id] is None or token2char[t_id] == (0, 0):
                    if token2char[t_id] is None:
                        b_start_score[t_id] = -10000
                        b_end_score[t_id] = -10000

                _, top_start_id = torch.topk(b_start_score, 2, dim=0)
                _, top_end_id = torch.topk(b_end_score, 2, dim=0)

                doc = batch[b_id]['doc']
                doc_offset = input_ids[b_id].index(102)

                res = all_tokens[top_start_id[0]:top_end_id[0] + 1]
                char_offset = token2char[doc_offset + 1][0]
                example_idx = batch[b_id]['example_idx']

                # first get cls type        
                cls_ind = int(torch.argmax(target_probs[b_id]).item())
                if cls_ind == 3:   # span
                    final_text = ''
                    value_type = 'span'
                else:
                    value_type = 'classification'
                    if cls_ind == 0:  # unans
                        final_text = ''
                    elif cls_ind == 1:  # yes
                        final_text = 'YES'
                    elif cls_ind == 2:  # no
                        final_text = 'NO'
                    else:
                        raise ValueError('{} is not a valid cls index'.format(cls_ind))

                #TODO: what are the options of ans_type?
                if cls_ind == 0 or not res or res[0] == "[CLS]" or res[0] == '[SEP]' or ans_type == 'yes_no':
                    prob = target_probs[b_id, cls_ind].item()
                    score = target_scores[b_id, cls_ind].item()
                    
                    prediction = {'supporting_fact': None,
                                  'value_type': value_type,
                                  'prob': prob,
                                  'start_end_prob': [prob, prob],
                                  'score': score,
                                  'start_end_score': [score, score],
                                  'value': final_text,
                                  'answer_start': -1,
                                  'example_idx': example_idx}
                    if not final_text:
                        prediction['missing_warning'] = True
                else:

                    s_prob = start_probs[b_id, top_start_id[0]].item()
                    e_prob = end_probs[b_id, top_end_id[0]].item()
                    s_logit = start_scores[b_id, top_start_id[0]].item()
                    e_logit = end_scores[b_id, top_end_id[0]].item()

                    prob = (s_prob + e_prob) / 2
                    score = (s_logit + e_logit) / 2

                    supporting_fact = None
                    if not merge_pred:
                        start_map = token2char[top_start_id[0].item()]
                        end_map = token2char[top_end_id[0].item()]
                        span = [start_map[0] - char_offset, end_map[1] - char_offset]

                        if final_text in ['YES', 'NO']:
                            supporting_fact = doc[span[0]: span[1]]
                            ans = final_text
                        else:
                            ans = doc[span[0]: span[1]]

                    else:
                        base_idx = batch[b_id]['base_idx']
                        orig_doc = batch[b_id]['orig_doc']
                        orig_token2char = batch[b_id]['orig_offset_mapping']

                        # map token index, then use offset mapping to map to original position
                        orig_start_map = orig_token2char[top_start_id[0].item() + base_idx - doc_offset - 1]
                        orig_end_map = orig_token2char[top_end_id[0].item() + base_idx - doc_offset - 1]
                        span = [orig_start_map[0], orig_end_map[1]]

                        if final_text in ['YES', 'NO']:
                            supporting_fact = doc[span[0]: span[1]]
                            ans = final_text
                        else:
                            ans = orig_doc[span[0]: span[1]]

                    prediction = {'value': ans,
                                  'supporting_fact': supporting_fact,
                                  'value_type': value_type,
                                  'answer_start': span[0],
                                  'answer_span': span,
                                  'prob': prob,
                                  'start_end_prob': [s_prob, e_prob],
                                  'score': score,
                                  'start_end_score': [s_logit, e_logit],
                                  'tokens': res,
                                  'example_idx': example_idx}

                results.append(prediction)

        # merge predictions
        if merge_pred:
            results = util.merge_predictions(results)

        return results


class MrcMultiSpanBioModel(ModelBase):
    def batch_predict(self, model_id, data, **kwargs):
        batch_size, merge_pred, stride = self._get_param(kwargs)
        if merge_pred:
            logger.warn('Merging prediction not implemented yet for {}'.format(self.__class__.__name__))

        tokenizer, model, device = self._load_model(model_id)

        features = util.convert_examples_to_features(tokenizer, data, self.max_input_length)

        results = []
        for batch in util.chunks(features, batch_size):
            padded = util.pad_batch(batch)
            input_ids, token_type_ids, attn_masks = padded

            with torch.no_grad():
                span_logits = model(torch.tensor(input_ids).to(device),
                                                 token_type_ids=torch.tensor(token_type_ids).to(device),
                                                 attention_mask=torch.tensor(attn_masks).to(device))
                span_probs = torch.softmax(span_logits, dim=2)
                span_logits = span_logits.detach().cpu().tolist()

            for b_id in range(len(batch)):
                all_tokens = tokenizer.convert_ids_to_tokens(input_ids[b_id])
                legal_length = batch[b_id]['length']
                b_span_logits = span_logits[b_id][0:legal_length]
                b_span_labels = np.argmax(b_span_logits, axis=1)
                token2char = batch[b_id]['offset_mapping']
                for t_id in range(legal_length):
                    if token2char[t_id] is None or token2char[t_id] == (0, 0):
                        b_span_labels[t_id] = 0
                doc = batch[b_id]['doc']
                doc_offset = input_ids[b_id].index(102)
                b_span_labels[:doc_offset+1] = 0
                
                b_span_indexes = util.get_span_from_ohe(b_span_labels)
                if not b_span_indexes:
                    prediction = {'missing_warning': True,
                                  'value': "", 
                                  'answer_start': -1}
                else:
                    char_offset = token2char[doc_offset + 1][0]
                    prediction = defaultdict(list)
                    for indexes in b_span_indexes:
                        res = all_tokens[indexes[0]:indexes[1] + 1]
                        probs = span_probs[b_id][indexes[0]:indexes[1] + 1][:,1].mean().tolist()
                        start_map = token2char[indexes[0]]
                        end_map = token2char[indexes[1]]
                        span = [start_map[0] - char_offset, end_map[1] - char_offset]
                        ans = doc[span[0]: span[1]]
                        prediction['value_type'] = 'multi_span'
                        prediction['value'].append(ans)
                        prediction['prob'].append(probs)
                        prediction['answer_start'].append(span[0])
                        prediction['answer_span'].append(span)
                        prediction['tokens'].append(res)

                results.append(prediction)

        return results


if __name__ == '__main__':
    use_gpu = False
    model = MrcModel('cn', use_gpu=use_gpu)
    data = [
        {'q': '张三是谁？', 'doc': '张三是一个铁匠。他很高。' * 20},
        {'q': '谁很高？', 'doc': '张三是一个铁匠。他很高。'},
        {'q': '如何开飞机？', 'doc': '张三是一个铁匠。他很高。'}

    ]
    res = model.batch_predict('roberta-wwm-ext-cmrc+drcd', data)
    print(res)

    data = [
        {'q': 'Who is Jack?', 'doc': 'Jack is a programmer. He is tall.'},
        {'q': 'Who is tall?', 'doc': 'Jack is a programmer. He is tall.'},
        {'q': 'How to cook pasta?', 'doc': 'Jack is a programmer. He is tall.'}

    ]
    res = model.batch_predict('spanbert-large-squad2', data)
    print(res)
