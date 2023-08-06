from soco_mrc.mrc_model import MrcModel, MrcClsModel, MrcClsMultiSpanModel, MrcClsFactModel, MrcMultiSpanBioModel
from soco_mrc.config import EnvVars


class MrcBase(object):
    def __init__(self, region=None, n_gpu=None):
        inputs = {
            'region': EnvVars.region if not region else region,
            'n_gpu': EnvVars.n_gpu if not n_gpu else n_gpu,
        }
        self.model = MrcModel(**inputs)
        self.cls_model = MrcClsModel(**inputs)
        self.cls_multi_span_model = MrcClsMultiSpanModel(**inputs)
        self.cls_fact_model = MrcClsFactModel(**inputs)
        self.multi_span_bio_model = MrcMultiSpanBioModel(**inputs)


    def _get_model_from_pattern(self, model_id):
        if 'cls-multi-span' in model_id:
            return self.cls_multi_span_model
        elif 'fact' in model_id:
            return self.cls_fact_model
        elif 'cls' in model_id:
            return self.cls_model
        elif 'bio' in model_id:
            return self.multi_span_bio_model
        else:
            return self.model

    def _get_model_from_task_type(self, task_type):
        task_type_model_map = {
            'span_cls_multi_span': self.cls_multi_span_model,
            'span_cls_fact': self.cls_fact_model,
            'span_cls': self.cls_model,
            'span_cls_bio': self.multi_span_bio_model,
            'span': self.model
        }

        return task_type_model_map.get(task_type, self.model)


    def batch_predict(self, model_id, data, **kwargs):
        task_type = kwargs.pop('task_type', None)
        if task_type:
            model = self._get_model_from_task_type(task_type)
        else:
            model = self._get_model_from_pattern(model_id)

        return model.batch_predict(model_id, data, **kwargs)

