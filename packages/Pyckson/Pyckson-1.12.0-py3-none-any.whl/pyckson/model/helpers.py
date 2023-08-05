from pyckson.const import PYCKSON_MODEL, PYCKSON_ATTR, set_cls_attr, get_cls_attr
from pyckson.helpers import is_pyckson
from pyckson.model.builder import PycksonModelBuilder
from pyckson.model.model import PycksonModel
from pyckson.parsers.provider import ParserProviderImpl
from pyckson.providers import ModelProvider
from pyckson.serializers.provider import SerializerProviderImpl


class ModelProviderImpl(ModelProvider):
    def get_or_build(self, obj_or_class) -> PycksonModel:
        if type(obj_or_class) is not type:
            return self.get_or_build(obj_or_class.__class__)
        if not is_pyckson(obj_or_class):
            self.set_model(obj_or_class)
        return get_cls_attr(obj_or_class, PYCKSON_MODEL)

    def set_model(self, cls):
        set_cls_attr(cls, PYCKSON_ATTR, True)
        model = PycksonModelBuilder(cls, SerializerProviderImpl(self), ParserProviderImpl(self)).build_model()
        set_cls_attr(cls, PYCKSON_MODEL, model)
