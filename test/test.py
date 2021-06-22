#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test
Description: 
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""
import json
import unittest
from unittest import TestCase

import requests


class Test(TestCase):

    def setUp(self) -> None:
        pass

    def test_test(self):
        url = "http://localhost:5000/test"
        params = {"test": "1"}
        res = requests.post(url, json=params)
        print(json.dumps(res.json(), indent=2, ensure_ascii=True))

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
