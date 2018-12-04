# -*- coding: utf-8 -*-


class Field(object):
    def __init__(self, name):
        self._name = name
        pass

    def __str__(self):
        return self._name
