# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
FileName: authenticate
Description: JWT 验证函数
Author: Connor Zhang
Email: zhangyue@datagrand.com
CreateTime: 2021-09-08
"""

from collections import namedtuple

import sanic
from sanic_jwt.exceptions import AuthenticationFailed

from authorization import AbstractAuthentication


class Authentication(AbstractAuthentication):
    def __init__(self, config: dict) -> None:
        super().__init__()
        user = namedtuple("user", ["username", "password", "user_id"])
        self.duser = user(username="admin", password="admin", user_id=123456)
        self.config = config
        self.config.update({"authenticate": self.authenticate, "extend_payload": self.payload_extender,
                            "add_scopes_to_payload": self.scopes_extender})

    async def authenticate(self, request: sanic.Request, *args, **kwargs):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if username == self.duser.username and password == self.duser.password:
            return {key: val for key, val in self.duser._asdict().items()}
        raise AuthenticationFailed("username or password error")

    @staticmethod
    async def payload_extender(payload: dict, user: dict, *args, **kwargs):
        payload.update({
            "username": user.get("username"),
            "department": "",
            "id": user.get("user_id"),
            "roles": [],
            "cabin_id": "User-1"
        })
        payload.pop("user_id", 1)

        return payload

    @staticmethod
    async def scopes_extender(user: dict, *args, **kwargs):
        return ["admin:read"]
