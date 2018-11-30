# -*- coding: utf-8 -*-

from .field import Field
from exceptions import TypeError


class Criterion(object):
    def __init__(self, field_name, operator, value):
        self.field_name = field_name
        self.operator = operator
        self.value = value

    def __and__(self, other):
        if isinstance(other, Criterion):
            return Domain('&', self, other)
        else:
            raise TypeError('Object must be a Criterion')

    def __or__(self, other):
        if isinstance(other, Criterion):
            return Domain('|', self, other)
        else:
            raise TypeError('Object must be a Criterion')

    def NOT(self):
        return Domain('|', self)

    def __str__(self):
        return str(self.dump())

    def dump(self):
        return self.field_name, self.operator, self.value


class Domain:
    def __init__(self, *args):
        self.domain = []
        for arg in args:
            if isinstance(arg, Criterion):
                self.domain.append(arg)
            elif isinstance(arg, (tuple, list)):
                for mini_arg in arg:
                    self.domain.append(mini_arg)
            else:
                pass

    def __add__(self, other):
        if isinstance(other, Domain):
            pass
        elif isinstance(other, Criterion):
            pass
        else:
            pass

    def __or__(self, other):
        if isinstance(other, Domain):
            pass
        elif isinstance(other, Criterion):
            pass
        else:
            pass

    def __str__(self):
        return str(self.dump())

    def dump(self):
        res = []
        for criterion in self.domain:
            if isinstance(criterion, Criterion):
                res.append(criterion.dump())
            elif isinstance(criterion, basestring):
                res.append(criterion)
        return res
