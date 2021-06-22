# 精简 docker build 构建层数

FROM dockerhub.datagrand.com/base_image/centos_py3:product_20200331

ADD ./ /sanic

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone && \
pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip && \
pip install -r /sanic/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /sanic/src

CMD ["sh", "runserver.sh"]
