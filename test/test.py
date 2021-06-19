#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test
Description: 
Author: ConnorZhang
Email: zhangyue@datagrand.com
CreateTime: 2021-05-24
"""
from unittest import TestCase
import unittest

import requests


class Test(TestCase):
    def setUp(self) -> None:
        pass

    def test_test(self):
        url = "http://localhost:6100/test"
        params = {"test": "1"}
        res = requests.post(url, json=params)
        print(res.json())

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
