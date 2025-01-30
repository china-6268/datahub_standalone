#!/bin/bash

set -e

# 动态获取当前路径并设置 docker-compose 文件路径
COMPOSE_FILE="$(pwd)/docker-compose.yml"

# 停止通过 docker-compose 管理的 gms 容器
stop_gms_container() {
  echo "正在停止 actions 容器..."
  if [ -f "$COMPOSE_FILE" ]; then
    # 停止 actions 容器
    docker compose -f "$COMPOSE_FILE" stop datahub-gms
    echo "gms 容器已停止。"
  else
    echo "错误：未找到 docker-compose.yml 文件，请确保路径正确。"
    exit 1
  fi
}

# 执行停止操作
stop_gms_container

