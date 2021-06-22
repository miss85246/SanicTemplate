#!/bin/sh
cd ..

TIME_NOW=$(date +%Y%m%d)
UUID=$(uuidgen)
UUID=${UUID##*-}
SUFFIX="${TIME_NOW}_${UUID}"

docker build -f docker/Dockerfile -t dockerhub.datagrand.com/databj/zhangyue/sanic_template:"${SUFFIX}" .
#docker push dockerhub.datagrand.com/databj/zhangyue/sanicTemplate:"${SUFFIX}"
