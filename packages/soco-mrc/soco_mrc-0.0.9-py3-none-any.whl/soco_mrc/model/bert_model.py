import torch
from torch import nn
from transformers import BertModel, BertPreTrainedModel

class BertForMrcCls(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.bert = BertModel(config)
        self.qa_outputs = nn.Linear(config.hidden_size, 2)
        self.cls_outputs = nn.Linear(config.hidden_size, 3)
        self.init_weights()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        sequence_output, pooled_output = self.bert(input_ids,attention_mask=attention_mask,token_type_ids=token_type_ids)
        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)
        target_logits = self.cls_outputs(pooled_output)

        return start_logits, end_logits, target_logits


class BertForMrcClsFact(BertPreTrainedModel):
    def __init__(self, config):
        """
        Do span/yes/no/noans classification and span prediction for span,yes/no(supporting fact)
        """
        super().__init__(config)
        self.bert = BertModel(config)
        self.qa_outputs = nn.Linear(config.hidden_size, 2)
        # target labels: 0:unknown, 1:yes, 2:no, 3: has answer
        self.cls_outputs = nn.Linear(config.hidden_size, 4)
        self.init_weights()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        sequence_output, pooled_output = self.bert(input_ids,attention_mask=attention_mask,token_type_ids=token_type_ids)
        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)
        target_logits = self.cls_outputs(pooled_output)

        return start_logits, end_logits, target_logits


class BertForMrcMultiSpanBio(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.bert = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.init_weights()


    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        """
        Do span prediction similar to BIO tagging, to enable outputing multiple spans
        """

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )

        sequence_output = outputs[0]
        sequence_output = self.dropout(sequence_output)
        logits = self.classifier(sequence_output)

        return logits