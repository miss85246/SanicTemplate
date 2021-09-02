#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: test
Description: 测试文件, 使用 sanic 自带的 test_client 进行测试
Author: {{cookiecutter.maintainer}}
Email: {{cookiecutter.email}}
CreateTime: {% now 'local' %}
"""
import json
import os
import sys
import unittest
from unittest import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.pop(0)
sys.path.append(os.path.join(BASE_DIR, "src"))


class Test(TestCase):

    def setUp(self) -> None:
        from server import server_app
        self.client = server_app.test_client
        self.resp = globals()

    # cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
    def test_authenticate(self) -> None:
        params = {"username": "admin", "password": "admin"}
        req, resp = self.client.post("/auth", json=params)
        self.resp["jwt"] = resp.json.get("access_token")
        print(json.dumps(resp.json, indent=2, ensure_ascii=True))
        # cookiecutter_flag {%- endif %}

    def test_test_endpoint(self):
        headers = {
            # cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
            "authorization": "Bearer " + self.resp["jwt"]
            # cookiecutter_flag {%- endif %}
        }
        params = {"test": "1"}
        req, resp = self.client.post("/test", json=params, headers=headers)
        print(json.dumps(resp.json, indent=2, ensure_ascii=True))

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
