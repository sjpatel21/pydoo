# -*- coding: utf-8 -*-


class Model(object):
    @property
    def name(self):
        return self._name

    def __init__(self, name, conn):
        """

        :param name: name of data model
        :param odoo: odoo connector core
        """
        if not isinstance(name, str) or not name:
            raise TypeError("Name of model invalid")
        self._name = name
        self._conn = conn

    def search(self, search_domain=None, offset=0, limit=None, order=None):
        """ search() takes a mandatory domain filter (possibly empty), and returns the database identifiers of all
        records matching the filter.
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
        return self._conn.search(self._name, search_domain=search_domain, offset=offset, limit=limit, order=order)

    def search_count(self, search_domain):
        """ Returns the number of records in the current model matching the provided domain.
        :param search_domain: A search domain.
        :type search_domain: list
        :return: number of records in the current model matching the provided domain.
        :rtype: int
        """
        return self._conn.search_count(self._name, search_domain)

    def read(self, ids, fields=None):
        """ Reads the requested fields for the records

        :param ids: a list of ids
        :type ids: list
        :param fields: list of field names to return (default is all fields)
        :return: a list of dictionaries mapping field names to their values, with one dictionary per record
        :rtype: list
        """
        return self._conn.read(self._name, ids, fields=fields)

    def fields_get(self, fields=None, attributes=None):
        """ Return the definition of each field.

        The _inherits'd fields are included. The string, help, and selection (if present) attributes are translated.
        list of description attributes to return for each field, all if empty or not provided

        :param fields: List of fields, [] for all fields
        :type fields: list
        :param attributes: field attribtutes to show
        :type attributes: list
        :return: The returned value is a dictionary (indiced by field name) of dictionaries.
        :rtype: dict
        """
        if attributes is None:
            attributes = ['string', 'help', 'type']
        return self._conn.fields_get(self._name, fields=fields, attributes=attributes)

    def search_read(self, search_domain=None, offset=0, limit=None, order=None, fields=None):
        """ search() takes a mandatory domain filter (possibly empty), and returns the database identifiers of all
        records matching the filter.
        :param search_domain: A search domain. Use an empty list to match all records : [('id', '>', 5), (...), ...]
        :type search_domain: list
        :param offset: number of results to ignore (default: none)
        :type offset: int
        :param limit: maximum number of records to return (default: all)
        :type limit: int
        :param order: sort string
        :type order: str
        :param fields: list of field names to return (default is all fields)
        :returns: at most limit records matching the search criteria
        :rtype: list
        """
        return self._conn.search_read(self._name, search_domain=search_domain, offset=offset, limit=limit,
                                      order=order, fields=fields)

    def create(self, **vals):
        """ The method will create a single record and return its database identifier
        :param vals: a mapping of fields to values
        :return: id of created record
        :rtype: int
        """
        return self._conn.create(self._name, **vals)

    def write(self, *ids, **vals):
        """ Records can be updated using write(), it takes a list of records to update and a mapping of updated fields
            to values similar to create()
        :param tuple ids: ids to write
        :param dict vals: values to write
        :return:
        """
        return self._conn.write(self._name, *ids, **vals)

    def unlink(self, *ids):
        """ Records can be deleted in bulk by providing their ids to unlink()
        :param ids: ids to delete
        :return:
        """
        return self._conn.unlink(self._name, *ids)

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
        return self._conn.check_access_rights(model_name, read=read, write=write, create=create, unlink=unlink,
                                              raise_exception=raise_exception)

    def exec_workflow(self, workflow_name, *args):
        """ Workflows can be moved along by sending them signals. 
        Instead of using the top-level execute_kw, signals are sent using exec_workflow.

        Signals are sent to a specific record, and possibly trigger a transition on the workflow instance 
        associated with the record.        
        :param workflow_name: name of workflow to execute
        :param args: parameters for the workflow
        :return:
        """
        return self._conn.exec_workflow(self._name, workflow_name, *args)

    def render_report(self, report_name, ids, raw=False):
        """

        :param report_name: name of report
        :param ids: ids of objects to get report from
        :param raw:
        :return:
        """
        return self._conn.render_report(report_name, ids, raw=raw)
