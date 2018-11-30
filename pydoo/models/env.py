# -*- coding: utf-8 -*-

from .model import Model


class Environment(object):
    def __init__(self, xmlrpc):
        super(Environment, self).__init__()
        self._queue = {}
        self._xmlrpc = xmlrpc

    @property
    def xmlrpc(self):
        return self._xmlrpc

    def __getitem__(self, name):
        return self._queue.setdefault(name, Model(name, self._xmlrpc))
