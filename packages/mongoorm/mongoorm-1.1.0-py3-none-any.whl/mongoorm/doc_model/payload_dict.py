import copy

from ..exceptions import DocModelErr, put_inst_exception


class PayloadDict(object):

    def _raise_attr_error(self, err_key):
        e = DocModelErr('object has no attribute {}'.format(err_key))
        raise put_inst_exception(e, self)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key: str, value):
        # print('__setattr__(self, key: str, value)', key, value)
        cls = self.__class__
        a = getattr(cls, key, None)
        if a is not None and isinstance(a, property):
            try:
                return a.__set__(self, value)
            except AttributeError:
                # todo if there is really AttributeError occurred in the method under @xxx.setter,
                #  it will be passed here
                pass

        return self.__setitem__(key, value)

    def __getitem__(self, k):
        try:
            # todo done!!!! big number to int?????
            if k in self.__payload__:
                return self.__payload__[k]
            else:
                field = self.__mappings__.get(k)
                if field is not None and field.has_rich_default:
                    if callable(field.rich_default):
                        r = field.rich_default()
                    else:
                        r = copy.deepcopy(field.rich_default)
                    return r
                else:
                    return self.__payload__[k]
        except KeyError:
            self._raise_attr_error(k)

    def __delitem__(self, key):
        del self.__payload__[key]

    def __setitem__(self, key, value):
        if self._use_schame and (key not in self.__mappings__) and (key not in self.__payload__):
            return self._raise_attr_error(key)
        self.__payload__[key] = value

    def pop(self, k, default=None):
        return self.__payload__.pop(k, default)

    def get(self, k, default=None):
        return self.__payload__.get(k, default)

    def items(self):
        return self.__payload__.items()

    def keys(self):
        return self.__payload__.keys()

    def values(self):
        return self.__payload__.values()

    def update(self, dict2):
        for k, v in dict2.items():
            self.__setitem__(k, v)

    def __iter__(self):
        raise DocModelErr('can not __iter__, maybe self.keys() or self.values() or self.items() ?')

    # todo python3 推荐 def, 不想写了, 先这么着吧
    __len__ = lambda x: len(x.__payload__)
    __contains__ = lambda x, i: i in x.__payload__
