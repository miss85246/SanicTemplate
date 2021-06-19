FROM dockerhub.datagrand.com/base_image/centos_py3:product_20200331
MAINTAINER zanyunfei <zanyunfei@datagrand.com>

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip

#install requires
ADD requirements.txt /sanic/requirements.txt
RUN pip install -r /sanic/requirements.txt -i https://pypi.douban.com/simple/

ADD src /sanic

WORKDIR /sanic

CMD sh runserver.sh
