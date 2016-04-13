# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest import main as unittest_main

from pydoo.core import OdooConnector


class TestOdooConnector(TestCase):
    def setUp(self):
        self.connector = OdooConnector(url="http://192.168.1.106/",
                                       db="test_gf_1zweifix",
                                       username="admin", password="admin")

    def test_login(self):
        self.connector.login()
        self.assertIsNot(self.connector.uid, False,
                         msg="User ID ist nicht richtig")

    def test_check_calling_method(self):
        ret = self.connector.call_method('res.partner', 'check_access_rights',
                                         'read', raise_exception=False)
        self.assertTrue(ret,
                        "User {} don't have access rights to model "
                        "res.partner".format(
                            self.connector._username))

    def test_search_method(self):
        ret = self.connector.search('res.partner', ['customer', '=', True])
        print "results of search method: " + str(ret)

    def test_search_method_with_pagination(self):
        ret = self.connector.search('res.partner', ['customer', '=', True],
                                    offset=5, limit=5)
        print "results of search method with pagination: " + str(ret)

    def test_read_records(self):
        ret = self.connector.read_records('res.partner',
                                          ['customer', '=', True], limit=1)
        print ret

    def test_fields_get(self):
        ret = self.connector.list_record_fields("res.partner",
                                                attributes=['string', 'help',
                                                            'type'])
        print ret

    def test_create_update_delete_partner(self):
        partner_id = self.connector.create_record("res.partner",
                                                  name="New partner",
                                                  type="contact")
        print "created partner with id: {}".format(partner_id)
        ret = self.connector.read_records("res.partner",
                                          ['id', '=', partner_id],
                                          fields=["name"])
        print "check name from db: {}".format(str(ret))
        ret = self.connector.update_record("res.partner", partner_id,
                                           name="New Partner 2")
        print "updated partner {} with new name".format(partner_id)
        ret = self.connector.read_records("res.partner",
                                          ['id', '=', partner_id],
                                          fields=["name"])
        print "check name from db: {}".format(str(ret))
        ret = self.connector.delete_record("res.partner", partner_id)
        print "removed partner with id {}".format(partner_id)
        ret = self.connector.read_records("res.partner",
                                          ['id', '=', partner_id],
                                          fields=["name"])
        print "check name from db: {}".format(str(ret))


if __name__ == '__main__':
    unittest_main()
