# -*- coding: utf-8 -*-


class Domain:
    def __init__(self, *args):
        self.criteria = []
        for arg in args:
            if isinstance(arg, Criterion):
                self.criteria.append(arg)

    def __str__(self):
        return str([str(criterion) for criterion in self.criteria])


class Criterion:
    def __init__(self, field_name, operator, value):
        self.field_name = field_name
        self.operator = operator
        self.value = value

    def __str__(self):
        return str([self.field_name, self.operator, self.value])
