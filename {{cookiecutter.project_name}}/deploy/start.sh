#!/bin/bash

# 服务启动脚本
if [[ $(pwd | xargs basename) == "deploy" ]]; then
    cd ../src || exit
else
    cd ./src || exit
fi

sanic server.server_app --no-access-logs --host "{{cookiecutter.server_bind_host}}" --port "{{cookiecutter.server_bind_port}}" --workers "{{cookiecutter.server_workers_count}}"

# 请尽量使用以上方式进行项目的启动， 特殊情况，可以使用以下启动方式：
# python3 server.py
