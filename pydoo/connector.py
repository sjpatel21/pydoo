# -*- coding: utf-8 -*-


from .core import OdooXmlRpc
from .models import Environment


class Odoo(object):
    def __init__(self, url, db, username, password, transport=None, encoding=None, verbose=0, allow_none=0,
                 use_datetime=0, context=None):
        """

        :param url:
        :param db:
        :param username:
        :param password:
        :param transport:
        :param encoding:
        :param verbose:
        :param allow_none:
        :param use_datetime:
        :param context:
        """
        xmlrpc = OdooXmlRpc(url, db, username, password, transport=transport, encoding=encoding, verbose=verbose,
                            allow_none=allow_none, use_datetime=use_datetime, context=context)
        self._models = {}
        self._env = Environment(xmlrpc)

    @property
    def xmlrpc(self):
        """

        :return:
        :rtype: OdooXmlRpc
        """
        return self._env.xmlrpc

    @property
    def env(self):
        """

        :return:
        :rtype: Environment
        """
        return self._env
