from .exceptions import DocModelErr
from .extensions.all_models import _all_models
from .meta import Meta
from .fields import _FieldBase
from .utils import log

doc_model_name = 'DocModel'


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        # log("构造{}对象".format(name), bases, attrs.get('__inheritance__'))
        if name == doc_model_name:
            return type.__new__(cls, name, bases, attrs)
        elif attrs.get('__inheritance__', False):
            if attrs.get('meta'):
                raise DocModelErr('Model {} error, when __inheritance__ = True, meta = Meta(*args, **kwargs) is forbidden'.format(name))
            attrs = handle_attr(name, attrs)
            update_mappings_from_bases(bases, attrs)
            return type.__new__(cls, name, bases, attrs)
        else:
            attrs['__inheritance__'] = False
            attrs = handle_attr(name, attrs)
            update_mappings_from_bases(bases, attrs)
            _new_cls_valid(name, attrs)
            m = type.__new__(cls, name, bases, attrs)

            # 冗余信息
            for name, field in m.__mappings__.items():
                field.name = name
                field.cls_model = m

            meta = attrs.get('meta')
            _all_models[(meta.db_alias, meta.collection, )] = m
            return m


def update_mappings_from_bases(bases, attrs):
    mappings = dict()
    for model in bases:
        d = getattr(model, '__mappings__', None)
        if isinstance(d, dict):
            mappings.update(d)

    mappings.update(attrs['__mappings__'])
    attrs['__mappings__'] = mappings
    return attrs


def handle_attr(name, attrs):
    mappings = dict()
    new_attrs = {}
    for k, v in attrs.items():
        if not isinstance(v, _FieldBase):
            new_attrs[k] = v
        else:
            mappings[k] = v
    attrs = new_attrs
    attrs['__mappings__'] = mappings

    return attrs


def _new_cls_valid(name, attrs):
    if not isinstance(attrs.get('meta'), Meta):
        raise DocModelErr('Model {} error, Meta class is required, or __inheritance__ = True??'.format(name))

    if '_id' not in attrs['__mappings__'] or (not attrs['__mappings__']['_id'].required):
        raise DocModelErr('Model {} error, _id is required as primary key, and must be required=True in kwargs'.format(name))

    meta = attrs.get('meta')
    if not meta.collection_name_repeated:
        k = (meta.db_alias, meta.collection, )
        if k in _all_models:
            raise DocModelErr('Model {} error, collection repeated, or collection_name_repeated = True??'.format(name))
        else:
            _all_models[k] = 1
