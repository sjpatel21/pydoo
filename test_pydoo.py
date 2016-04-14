# -*- coding: utf-8 -*-

import pprint
from unittest import TestCase
from unittest import main as unittest_main

from pydoo.core import OdooXmlRpc

pp = pprint.PrettyPrinter(indent=4)


class TestOdooConnector(TestCase):
    def setUp(self):
        self.connector = OdooXmlRpc(url="http://10.0.3.21:8069",
                                    db="dealclub_test_db",
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
        ret = self.connector.read_records('product.template',
                                          ['default_code', '=', 10167220])
        pp.pprint(ret[0].get('id'))

    def test_fields_get(self):
        ret = self.connector.get_record_fields("res.partner",
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

    def test_get_fields_product(self):
        ret = self.connector.list_record_fields("product.template",
                                                attributes=['string', 'help',
                                                            'type'])
        pp.pprint(ret)

    def test_create_order(self):
        order_id = self.connector.create_record("sale.order", partner_id=33, )
        print order_id
        order_line_id = self.connector.create_record("sale.order.line",
                                                     order_id=order_id,
                                                     product_id=1277,
                                                     product_uom_qty=2,
                                                     price_unit=12,
                                                     tax_id=[(4, 12, 0)],
                                                     product_uom=1,
                                                     type="make_to_stock",
                                                     state="draft",
                                                     name="test")
        print order_line_id


if __name__ == '__main__':
    unittest_main()
