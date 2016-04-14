# -*- coding: utf-8 -*-

import xmlrpclib
from socket import error as SocketError
from threading import Event


class OdooXmlRpc(object):
    """ Connect with odoo over XML-RPC protocol

    """
    def __init__(self, url, db, username, password):
        """

        :param url: URL of the odoo server (with http://)
        :param db: database name
        :param username: user name
        :param password: password of the user
        :return:
        """
        self._db = db
        self._username = username
        self._password = password
        if url[-1] == '/':
            self._url = url[:-1]
        else:
            self._url = url
        self.uid = None
        self._common = None
        self._models = None
        self._is_logged = Event()
        self._is_logged.clear()

    def login(self):
        try:
            self._common = xmlrpclib.ServerProxy(
                "{}/xmlrpc/2/common".format(self._url))
            self._models = xmlrpclib.ServerProxy(
                '{}/xmlrpc/2/object'.format(self._url))
        except xmlrpclib.ProtocolError:
            # false url
            raise
        except SocketError:
            # Error: Odoo server unavailable
            # Internet problem
            raise

        try:
            self.uid = self._common.authenticate(self._db, self._username,
                                                 self._password, {})
        except SocketError:
            # Error: Odoo server unavailable
            # Internet problem
            print("Server unavailable")
            raise
        except Exception:
            # Database not exist
            # Username not exist
            # Password false
            raise
        self._is_logged.set()

    def _execute_kw(self, model, method, *args, **kwargs):
        """ execute a method on a model

        :param model: model name
        :param method: method name
        :param args: parameter as list
        :param kwargs: parameter as dict
        :return: response from odoo server
        """
        if not self._is_logged.is_set():
            # check logged?
            self.login()
        # args is a tuple -> convert to a list
        return self._models.execute_kw(self._db, self.uid, self._password,
                                       model, method, list(args), kwargs)

    def call_method(self, model, method, *args, **kwargs):
        """ recall _execute_kw

        :param model:
        :param method:
        :param args:
        :param kwargs:
        :return:
        """
        return self._execute_kw(model, method, *args, **kwargs)

    def search(self, model, *args, **kwargs):
        """ list records of a model

        :param model: model name
        :param offset: beginning index of results
        :param limit: maximum records to return
        :param args: list of domain filter
        (https://www.odoo.com/documentation/9.0/reference/orm.html#reference
        -orm-domains)
        :return: database ids of all records matching the filter
        """
        return self._execute_kw(model, "search", list(args), **kwargs)

    def search_count(self, model, *args):
        return self._execute_kw(model, "search_count", list(args))

    def read_records_from_ids(self, model, *ids):
        return self._execute_kw(model, "read", list(ids))

    def read_records(self, model, *args, **kwargs):
        return self._execute_kw(model, "search_read", list(args), **kwargs)

    def get_record_fields(self, model, *args, **kwargs):
        return self._execute_kw(model, "fields_get", *args, **kwargs)

    def create_record(self, model, **values):
        return self._execute_kw(model, "create", values)

    def update_records(self, model, *ids, **values):
        """ update records

        :param model: model name
        :param ids: tuple of record ids to update
        :param values: dict of values to update
        :return:
        """
        return self._execute_kw(model, "write", list(ids), values)

    def get_record_names(self, model, *ids):
        return self._execute_kw(model, "name_get", list(ids))

    def delete_records(self, model, *ids):
        """ delete records with id in the ids

        :param model: model name
        :param ids: tuple of ids to delete
        :rtype:
        :return:
        """
        return self._execute_kw(model, "unlink", list(ids))
