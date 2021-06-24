#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test
Description: 测试文件, 使用 sanic 自带的 test_client 进行测试
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""
import json
import unittest
from unittest import TestCase

from server import server_app


class Test(TestCase):

    def setUp(self) -> None:
        self.client = server_app.test_client

    def test_by_client(self):
        params = {"test": "1"}
        req, resp = self.client.post("/test", json=params)
        print(json.dumps(resp.json, indent=2, ensure_ascii=True))

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
