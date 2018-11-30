# -*- coding: utf-8 -*-

import unittest

from pydoo.core import OdooXmlRpc


class TestOdooCore(unittest.TestCase):
    def test_connection(self):
        try:
            odoo_xml_rpc = OdooXmlRpc('10.0.3.21', 'test_db', 'admin', 'admin')
            odoo_xml_rpc.call_method(name="sdasd")
        except Exception:
            self.assertTrue(True)
        self.assertTrue(False)
