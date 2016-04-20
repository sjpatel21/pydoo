# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class OdooModel(object):
    __metaclass__ = ABCMeta
    __data = {}

    @abstractproperty
    def __model(self):
        return ""

    @abstractproperty
    def __attributes(self):
        return {}

    def __init__(self):
        pass
