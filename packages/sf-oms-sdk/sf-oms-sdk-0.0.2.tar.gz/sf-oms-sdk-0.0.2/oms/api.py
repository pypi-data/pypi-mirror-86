#!/usr/bin/python3
# @Time    : 2020-11-23
# @Author  : Kevin Kong (kfx2007@163.com)

from .comm import Comm
from .product import Product
from .stock import Stock


class OMS(object):

    def __init__(self, client_code, checkword, sandbox=True):
        self.clientcode = client_code
        self.checkword = checkword
        self.sandbox = sandbox

    comm = Comm()
    product = Product()
    stock = Stock()
