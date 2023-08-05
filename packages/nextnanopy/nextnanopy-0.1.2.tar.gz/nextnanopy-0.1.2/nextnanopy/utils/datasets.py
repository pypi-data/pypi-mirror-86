from copy import deepcopy


class Data(object):
    params = ['name', 'value']

    def __init__(self, name, value):
        self.name = str(name)
        self.value = value

    def parameters(self):
        dict_ = {}
        for param in self.params:
            value = getattr(self, param)
            dict_[param] = value
        dict_ = deepcopy(dict_)
        return dict_

    def __repr__(self):
        cname = self.__class__.__name__
        out = f'{cname}("{self.name}",...)'
        return out


class Variable(Data):
    params = ['name', 'value', 'label', 'unit', 'metadata']

    def __init__(self, name, value, label='', unit='', metadata={}):
        self.name = str(name)
        self.value = value
        if label:
            label = name
        self.label = str(label)
        self.unit = str(unit)
        self.metadata = metadata

    def get_value(self):
        value = deepcopy(self.value)
        return value


class Coord(Data):
    params = ['name', 'value', 'label', 'unit', 'offset', 'dim', 'metadata']

    def __init__(self, name, value, dim, label='', unit='', offset=0, metadata={}):
        self.name = str(name)
        self.value = value
        self.dim = int(dim)
        if label:
            label = name
        self.label = str(label)
        self.unit = str(unit)
        self.offset = float(offset)
        self.metadata = metadata
        self.valueo = self.get_value(use_offset=True)

    def get_value(self, use_offset=False):
        value = deepcopy(self.value)
        if use_offset:
            value += self.offset
        return value


class InputVariable(Data):
    params = ['name', 'value', 'label', 'unit', 'comment', 'text', 'metadata']
    var_char = ''
    com_char = ''

    def __init__(self, name, value, label='', unit='', comment='', metadata={}):
        self.name = str(name)
        self.value = value
        if label:
            self.label = name
        self.unit = unit
        self.comment = comment
        self.metadata = metadata

    def get_value(self):
        value = deepcopy(self.value)
        return value

    @property
    def text(self):
        t = f'{self.var_char}{self.name} = {self.value}'
        if self.comment:
            t = f'{t} {self.com_char} {self.comment}'
        return t


