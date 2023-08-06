#!/usr/bin/python3
# @Time    : 2020-11-23
# @Author  : Kevin Kong (kfx2007@163.com)

# 商品接口

from oms.comm import Comm


class Product(Comm):

    def define_product(self, CompanyCode, Items):
        """
        客户系统通过该接口向顺丰发送商品信息，该接口必须先于入库单接口、出库单接口调用。 

        params:
        param CompanyCode: 货主编码(由顺丰提供)
        param SkuNo: 商品编码
        param ItemName: 商品名称
        """
        data = {
            "service":"ITEM_SERVICE",
            "ItemRequest": {
                "CompanyCode": CompanyCode,
                "Items": Items
            }
        }
        return self.post(data)
