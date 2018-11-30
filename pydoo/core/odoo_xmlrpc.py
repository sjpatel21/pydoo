# -*- coding: utf-8 -*-
"""
XmlRpc API Client for Odoo 8, 9 (not tested for odoo 10)

"""
import xmlrpclib
from socket import error as SocketError
import ssl


class AuthException(Exception):
    """ Authentication Exception
    """
    pass


class OdooXmlRpc(object):
    """ Connect with odoo over XML-RPC protocol

    """

    def __init__(self, url, db, username, password, transport=None, encoding=None, verbose=0, allow_none=0,
                 use_datetime=0, context=None, use_ssl=False):
        """

        :param str url: URL of Odoo Server
        :param str db: data base name
        :param str username: login username
        :param str password: login password
        :param transport:
        :param encoding:
        :param verbose:
        :param allow_none:
        :param use_datetime:
        :param context:
        :param use_ssl: Use SSL connection or not
        :type use_ssl: bool
        """

        if "http" not in url:
            raise ValueError("URL must contain http or https")
        if url[-1] == '/':
            url = url[:-1]
        else:
            url = url

        if use_ssl:
            context = ssl._create_unverified_context()

        try:
            self._common = xmlrpclib.ServerProxy("{}/xmlrpc/2/common".format(url), transport=transport,
                                                 encoding=encoding, verbose=verbose, allow_none=allow_none,
                                                 use_datetime=use_datetime, context=context)
            self._models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), transport=transport,
                                                 encoding=encoding, verbose=verbose, allow_none=allow_none,
                                                 use_datetime=use_datetime, context=context)
            self._report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(url))
        except xmlrpclib.ProtocolError:
            # false url
            raise
        except SocketError:
            # Error: Odoo server unavailable
            # Internet problem
            raise

        self._db = db
        self._username = username
        self._password = password
        self._uid = None

    @property
    def is_logged(self):
        """ is logged in server?
        """
        if not self._uid:
            return False
        return True

    def login(self, username=None, password=None):
        """
            Set new username, password and login
        :param username:
        :param password:
        :return:
        """
        self._username = username if username is not None else self._username
        self._password = password if password is not None else self._password
        self._login()

    def _login(self):
        """
            Login to get uid (use saved username and password)
        """
        try:
            self._uid = self._common.authenticate(self._db, self._username, self._password, {})
        except SocketError:
            # Error: Odoo server unavailable
            # Internet problem
            raise
        except Exception:
            # Database not exist
            # Username not exist
            # Password false
            raise
        if not self.is_logged:
            raise AuthException("Username or password wrong")

    def _execute_kw(self, model, method, args, kwargs):
        """ execute a method on a model

        :param str model: model name
        :param str method: method name
        :param list args: parameter as list
        :param dict kwargs: parameter as dict
        :return: response from odoo server
        """
        if not self.is_logged:
            self._login()
        return self._models.execute_kw(self._db, self._uid, self._password,
                                       model, method, args, kwargs)

    def execute_kw(self, model, method, *args, **kwargs):
        """

        :param model:
        :param method:
        :param args:
        :param kwargs:
        :return:
        """
        return self._execute_kw(model, method, list(args), kwargs)

    def search(self, model_name, search_domain=None, offset=0, limit=None, order=None):
        """ search() takes a mandatory domain filter (possibly empty), and returns the database identifiers of all
        records matching the filter.
        :param model_name: name of model to search
        :type model_name: str
        :param search_domain: A search domain. Use an empty list to match all records : [('id', '>', 5), (...), ...]
        :type search_domain: list
        :param offset: number of results to ignore (default: none)
        :type offset: int
        :param limit: maximum number of records to return (default: all)
        :type limit: int
        :param order: sort string
        :type order: str
        :returns: at most limit records matching the search criteria
        :rtype: list
        """
        attrs = {}
        if search_domain is None:
            search_domain = []
        if limit is not None:
            attrs['limit'] = limit
        if order is not None:
            attrs['order'] = order
        return self.execute_kw(model_name, "search", search_domain, offset=offset, **attrs)

    def search_count(self, model_name, search_domain=None):
        """Returns the number of records in the current model matching the provided domain.
        :param: model_name: name of model to search
        :type model_name: str
        :param search_domain: A search domain.
        :type search_domain: list
        :return: number of records in the current model matching the provided domain.
        :rtype: int
        """
        if search_domain is None:
            search_domain = []
        return self.execute_kw(model_name, "search_count", search_domain)

    def read(self, model_name, ids, fields=None):
        """

        :param str model_name: model name
        :param ids: ids of the rows to read
        :param list fields:
        :return:
        :rtype: list
        """
        if fields is None:
            fields = []
        return self.execute_kw(model_name, "read", ids, fields=fields)

    def fields_get(self, model_name, fields=None, string=False, help=False, type_=False):
        """ Return the definition of each field.

        The _inherits'd fields are included. The string, help, and selection (if present) attributes are translated.
        list of description attributes to return for each field, all if empty or not provided

        :param model_name: name of model
        :type model_name: str
        :param fields: List of fields, [] for all fields
        :type fields: list
        :param string: the field's label
        :type string: bool
        :param help: a help text if available
        :type help: bool
        :param type_: to know which values to expect, or to send when updating a record
        :type type_: bool
        :return: The returned value is a dictionary (indiced by field name) of dictionaries.
        :rtype: dict
        """
        if fields is None:
            fields = []
        attrs = []
        if string:
            attrs.append('string')
        if help:
            attrs.append('help')
        if type_:
            attrs.append('type')
        return self.execute_kw(model_name, "fields_get", fields, attributes=attrs)

    def search_read(self, model_name, search_domain=None, offset=0, limit=None, order=None, fields=None):
        """ search() takes a mandatory domain filter (possibly empty), and returns the database identifiers of all
        records matching the filter.
        :param model_name: name of model to search
        :type model_name: str
        :param search_domain: A search domain. Use an empty list to match all records : [('id', '>', 5), (...), ...]
        :type search_domain: list
        :param offset: number of results to ignore (default: none)
        :type offset: int
        :param limit: maximum number of records to return (default: all)
        :type limit: int
        :param order: sort string
        :type order: str
        :param count: if True, only counts and returns the number of matching records (default: False)
        :type count: int
        :param fields: list of field names to return (default is all fields)
        :returns: at most limit records matching the search criteria
        :rtype: list
        """
        if search_domain is None:
            search_domain = []
        if fields is None:
            fields = []
        attrs = {}
        if search_domain is None:
            search_domain = []
        if limit is not None:
            attrs['limit'] = limit
        if order is not None:
            attrs['order'] = order
        return self.execute_kw(model_name, "search_read", search_domain, offset=offset, fields=fields, **attrs)

    def create(self, model_name, **kwargs):
        """ create a single record and return its database identifier
        :param str model_name: name of model
        :param vals: a mapping of fields to values
        :return: id of created record
        :rtype: int
        """

        # TODO: test if this method can create more than 1 record
        return self.execute_kw(model_name, "create", [kwargs])

    def write(self, model_name, *ids, **vals):
        """ Records can be updated using write(), it takes a list of records to update and a mapping of updated fields
            to values similar to create()
        :param str model_name: name of model
        :param tuple ids: ids to write
        :param dict vals: values to write
        :return:
        """
        return self.execute_kw(model_name, "write", list(ids), vals)

    def unlink(self, model_name, *ids):
        """ delete records with id in the ids

        :param model_name: model name
        :param ids: tuple of ids to delete
        :rtype:
        :return:
        """
        return self.execute_kw(model_name, "unlink", list(ids))

    def check_access_rights(self, model_name, read=False, write=False, create=False, unlink=False,
                            raise_exception=False):
        """

        :param model_name:
        :param read:
        :param write:
        :param create:
        :param unlink:
        :param raise_exception:
        :return:
        """
        attrs = []
        if read:
            attrs.append('read')
        if write:
            attrs.append('write')
        if create:
            attrs.append('create')
        if unlink:
            attrs.append('unlink')
        return self.execute_kw(model_name, *attrs, raise_exception=raise_exception)

    def exec_workflow(self, model_name, workflow_name, *args):
        """ Workflows can be moved along by sending them signals.
        Instead of using the top-level execute_kw, signals are sent using exec_workflow.

        Signals are sent to a specific record, and possibly trigger a transition on the workflow instance
        associated with the record.
        :param model_name: name of model
        :param workflow_name: name of workflow to execute
        :param args: parameters for the workflow
        :return:
        """

        return self._models.exec_workflow(self._db, self._uid, self._password, model_name, workflow_name, *args)

    def render_report(self, report_name, ids, raw=False):
        """

        :param report_name: name of report
        :param ids: ids of objects to get report from
        :param raw:
        :return:
        """
        result = self._report.render_report(self._db, self._uid, self._password, report_name, ids)
        if raw:
            return result
        return result['result'].decode('base64')
