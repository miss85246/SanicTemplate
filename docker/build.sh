#!/bin/bash
SnakeProjectName=""
ImageTag=""
ProjectName="SanicTemplate"
PushSwitch="True"
TagPrefix="dockerhub.datagrand.com/databj/sanic_template"
# 驼峰命名法转蛇形命名法
camel_to_snake() {
    NameArray=()
    if [ "$(echo ${ProjectName} | awk '{print tolower($0)}')" != ${ProjectName} ]; then
        for ((i = 0; i <= $(echo ${ProjectName} | awk '{print length($0)}') - 1; i = i + 1)); do
            original_case=${ProjectName:${i}:1}
            lowercase=$(echo ${original_case} | awk '{print tolower($0)}')
            if [ ${original_case} == "${lowercase}" ]; then
                NameArray[i]=${original_case}
            elif [ "${i}" == 0 ]; then
                NameArray[i]="${lowercase}"
            else
                NameArray[i]="_${lowercase}"
            fi
        done
        for char in "${NameArray[@]}"; do
            SnakeProjectName="${SnakeProjectName}${char}"
        done
    else
        SnakeProjectName=$ProjectName
    fi
}

# 推送 Dockers 镜像
push_image() {
    if [[ "${PushSwitch}" == "True" ]]; then
        echo "推送镜像..."
        docker push "${ImageTag}"
        echo "镜像推送成功，镜像名称：${ImageTag}"
    else
        echo "镜像构建成功，镜像名称：${ImageTag}"
    fi
}

# 创建 Docker 镜像
build_image() {
    Uuid="$(uuidgen)"
    Suffix="${SnakeProjectName}:$(date +%Y%m%d)_${Uuid##*-}"
    if [[ ${TagPrefix: -1} == "/" ]]; then
        TagPrefix=${TagPrefix%?}
    fi
    ImageTag=$(echo "${TagPrefix}/${Suffix}" | awk '{print tolower($0)}')
    echo "docker build -f docker/Dockerfile -t ${ImageTag} ."
    docker build -f docker/Dockerfile -t "${ImageTag}" .
}

# 判断当前路径
judge_now_path() {
    if [[ $(pwd | xargs basename) == "docker" ]]; then
        cd .. || exit
    else
        cd . || exit
    fi
}

# 主流程
main() {
    echo "判断当前路径..."
    judge_now_path
    echo "转换项目名称格式..."
    camel_to_snake
    echo "构建 Docker 镜像..."
    build_image
    push_image
}

main
