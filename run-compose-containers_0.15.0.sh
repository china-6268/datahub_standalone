#!/bin/bash
# start-compose-containers.sh

set -e

# 动态获取当前路径并设置 docker-compose 文件路径
COMPOSE_FILE="$(pwd)/docker-compose.yml"

# 启动通过 docker-compose 管理的容器
start_compose_containers() {
  echo "正在启动通过 docker-compose 管理的容器..."
  if [ -f "$COMPOSE_FILE" ]; then
    docker compose -f "$COMPOSE_FILE" up -d
    echo "通过 docker-compose 管理的容器已启动。"
  else
    echo "错误：未找到 docker-compose.yml 文件，请确保路径正确。"
    exit 1
  fi
}

# 执行启动操作
start_compose_containers

