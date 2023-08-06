#!/usr/bin/python3
# @Time    : 2020-11-23
# @Author  : Kevin Kong (kfx2007@163.com)

import unittest
from oms.api import OMS


class TestComm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oms = OMS("bvW2Fcx8Hb1OYzZaL2mY8A==",
                      "Pa2zfPtcCIvmhxYkfw5Bj6JgPmx63s4i")

    def test_define_product(self):
        """Test Comm"""
        res = self.oms.product.define_product("COMMONCOMPANY", [
            {"Item": {
                "SkuNo": "1111",
                "ItemName": "2222"
            }}
        ])
        self.assertEqual(res['result'], 0, res)

    def test_delivery(self):
        """测试出库"""
        data = [
            {
                "SaleOrder": {
                    "SFOrderType": "10",
                    "ErpOrder": "SO00001",
                    "OrderReceiverInfo": {
                        "ReceiverCompany": "个人",
                        "ReceiverName": "张三",
                        "ReceiverZipCode": "100000",
                        "ReceiverMobile": "15111112222",
                        "ReceiverCountry": "中国",
                        "ReceiverAddress": "北京市朝阳区大屯路1号"
                    },
                    "OrderSenderInfo": {
                        "SenderCompany": "华硕",
                        "SenderMobile": "18512345678"
                    },
                    "OrderItems": [
                        {
                            "OrderItem": {
                                "SkuNo": "1111",
                                "ItemQuantity": "1",
                            }
                        }
                    ]
                }
            }
        ]
        res = self.oms.stock.delivery("COMMONCOMPANY", data)
        self.assertEqual(res['result'], 0, res)


if __name__ == "__main__":
    unittest.main()
