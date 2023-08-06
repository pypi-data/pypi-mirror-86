#!/usr/bin/python3
# @Time    : 2020-11-23
# @Author  : Kevin Kong (kfx2007@163.com)

import base64
from hashlib import md5
from lxml import etree
import inspect
from itertools import zip_longest
from functools import partial
import requests

URL = "http://bsp.sit.sf-express.com:8080/bsp-wms/OmsCommons"

class Comm(object):
    """封装公共请求"""

    def __get__(self, instance, owner):
        self._clientcode = instance.clientcode
        self._checkword = instance.checkword
        self._sandbox = instance.sandbox
        return self

    def gen_verifycode(self, data):
        """
        生成校验码
        参数：
        data: 传输的报文
        """
        s = "{}{}".format(data, self._checkword)
        return base64.b64encode(md5(s.encode("utf-8")).digest()).decode("utf-8")

    def gen_xmldata(self, data):
        """
        生成xml报文
        """
        print('---xml data-----')
        print(data)
        root = etree.Element("Request")
        root.set("service", data.pop("service", None))
        root.set("lang", data.get("lang", "zh-CN"))
        head = etree.Element("Head")
        access_code = etree.Element("AccessCode")
        access_code.text = data.get("clientcode", self._clientcode)
        head.append(access_code)
        check_word = etree.Element("Checkword")
        check_word.text = data.get("checkword", self._checkword)
        head.append(check_word)
        root.append(head)
        body = etree.Element("Body")

        self._org_xml(body, data)
        root.append(body)
        return etree.tostring(root, xml_declaration=False, encoding="UTF-8").decode("utf-8")

    def _org_xml(self, root, data):
        """组织xml"""
        for key, value in data.items():
            sub = etree.Element(key)
            if type(value) is dict:
                self._org_xml(sub, value)
            elif type(value) is list:
                for v in value:
                    self._org_xml(sub, v)
            else:
                sub.text = str(value) if value else ""
            root.append(sub)
        return root

    def _parse(self, root):
        data = {}
        # 如果所有node同名，应该使用List存储
        if len(set([node.tag for node in root.getchildren()])) < len(root.getchildren()):
            first = root.getchildren()[0]
            data[first.tag] = []
            for node in root.getchildren():
                record = {}
                for att, val in node.items():
                    record[att] = val
                data[first.tag].append(record)
                # 获取子节点
                if len(node.getchildren()):
                    # for n in node.getchildren():
                    data[node.tag] = self._parse(node)

        else:
            for node in root.getchildren():
                data[node.tag] = {}
                # 获取属性和属性值
                for att, val in node.items():
                    data[node.tag][att] = val
                # 获取子节点
                if len(node.getchildren()):
                    # for n in node.getchildren():
                    data[node.tag] = self._parse(node)
                else:
                    data[node.tag] = node.text
        # 处理本节点的属性
        for att, val in root.items():
            data[att] = val
        return data

    # def get_jsondata(self,data):
    #     return {
    #         "msgData": data['data'],
    #         "msgmsgDigest": self.gen_verifycode(data)
    #     }

    def parse_response(self, data):
        """
        解析响应结果
        """
        print('---------')
        print(data.decode('utf-8'))
        res = {}
        root = etree.fromstring(data)
        head = root.xpath("//Head")[0].text
        if head == "ERR":
            # 发生错误，停止解析
            res["result"] = 1
            res["msg"] = root.xpath("//Error")[0].text

        if head == "OK":
            # 返回成功
            body = root.xpath("//Body")[0]
            data = self._parse(body)
            res["result"] = 0
            res["data"] = data

        if head == "PART":
            # 系统调用成功 但是数据不对
            body = root.xpath("//Body")[0]
            data = self._parse(body)
            res['result'] = 1
            res['data'] = data

        return res

    def post(self, data):
        """
        提交请求
        """
        xml = self.gen_xmldata(data)
        post_data = {
            "logistics_interface": xml,
            "data_digest": self.gen_verifycode(xml)
        }

        response = requests.post(URL, post_data)
        return self.parse_response(response.content)
