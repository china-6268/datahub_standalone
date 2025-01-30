#!/bin/bash

# 设置镜像名称和标签
IMAGE_NAME="custom-gms-image"
TAG="0.14.1"

# 构建 Docker 镜像，使用指定的 Dockerfile_custom
docker build -f Dockerfile_custom -t ${IMAGE_NAME}:${TAG} .

# 查看构建的镜像
docker images | grep ${IMAGE_NAME}

# 可选：将镜像推送到 Docker Hub 或其他仓库
# docker tag ${IMAGE_NAME}:${TAG} your_dockerhub_username/${IMAGE_NAME}:${TAG}
# docker push your_dockerhub_username/${IMAGE_NAME}:${TAG}

