# -*- coding: utf-8 -*-

from .odoo_model import OdooModel


class Product(OdooModel):
    @property
    def __model(self):
        return "product.product"

    @property
    def __attributes(self):
        return {'name': str}


class ProductTemplate(object):
    @property
    def __model(self):
        return "product.template"

    @property
    def __attributes(self):
        return {'name': str}
