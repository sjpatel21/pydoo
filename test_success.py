# -*- coding: utf-8 -*-

import unittest

from pydoo.core import OdooXmlRpc
import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestOdooCore(unittest.TestCase):
    def setUp(self):
        self.odoo_core = OdooXmlRpc('http://10.10.10.13:8069', 'test_bundle', 'admin', 'Tqa.!8E5oE$p42Tug|Ir')

    def test_login(self):
        self.assertFalse(self.odoo_core.is_logged)
        self.odoo_core._login()
        self.assertTrue(self.odoo_core.is_logged)

    def test_search(self):
        pass

    def test_search_count(self):
        pass

    def test_read(self):
        pass

    def test_fields_get(self):
        pass

    def test_search_read(self):
        ret = self.odoo_core.search_read("product.template", filters=[["id", "=", 10]])
        for row in ret:
            pp.pprint(row)
