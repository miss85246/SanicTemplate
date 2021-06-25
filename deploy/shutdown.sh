#!/bin/bash

# 服务停止脚本

ps -ef | grep "[sanic] server.server_app" |awk '{print $2}' |xargs kill -9
