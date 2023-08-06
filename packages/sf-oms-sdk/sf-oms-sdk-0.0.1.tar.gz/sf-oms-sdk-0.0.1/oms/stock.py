#!/usr/bin/python3
# @Time    : 2020-11-24
# @Author  : Kevin Kong (kfx2007@163.com)

# 出库单

from .comm import Comm

SfOrderTypes = [
    ('10', '销售订单'),
    ('20', '返厂订单'),
    ('30', '换货订单'),
    ('40', '调拨订单'),
    ('50', '退仓订单'),
    ('90', 'NPR订单')
]


class Stock(Comm):

    def delivery(self, CompanyCode, Orders):
        """
        提供给客户下发出库单数据

        params:
        param CompanyCode: 货主编码(由顺丰提供)
        param Orders: 订单信息
        """

        data = {
            "service": "SALE_ORDER_SERVICE",
            "SaleOrderRequest": {
                "CompanyCode": CompanyCode,
                "SaleOrders": Orders
            }
        }

        return self.post(data)
