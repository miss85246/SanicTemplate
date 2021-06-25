#!/bin/sh
cd ..
PUSH_SWITCH=false
echo "${PUSH_SWITCH}"
PROJECT_NAME="sanic_template"
TAG_PREFIX="dockerhub.datagrand.com/databj/zhangyue"
UUID="$(uuidgen)"
SUFFIX="${PROJECT_NAME}:$(date +%Y%m%d)_${UUID##*-}"
IMAGE_TAG="${TAG_PREFIX}/${SUFFIX}"

docker build -f docker/Dockerfile -t "${IMAGE_TAG}" .

if ${PUSH_SWITCH}; then
  docker push IMAGE_TAG
fi
