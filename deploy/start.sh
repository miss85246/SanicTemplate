#!/bin/bash

# 服务启动脚本
if [[ $(pwd | xargs basename) == "deploy" ]]; then
    cd ../src || exit
else
    cd ./src || exit
fi

sanic server.server_app --no-access-logs --host "0.0.0.0" --port "5000" --workers "4"

# 请尽量使用以上方式进行项目的启动， 特殊情况，可以使用以下启动方式：
# python3 server.py
