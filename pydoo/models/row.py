# -*- coding: utf-8 -*-


class Row(object):
    """

    """

    def __init__(self, row=None):
        """

        :param row: Row to copy data
        """
        self._data = {}
        if row is None:
            self._modified_data = {}
        elif isinstance(row, Row):
            self._modified_data = row.get_data()

    def __getitem__(self, field):
        """

        :param field: field name
        :type field: str
        :return: value of item oder None
        """
        return self._data.get(field, None)

    def __setitem__(self, field, value):
        """

        :param field: field name
        :type field: str
        :param value:
        :return: None
        """
        self._data[field] = value

    def get_data(self):
        """

        :return: intern data
        :rtype: dict
        """
        return self._data
