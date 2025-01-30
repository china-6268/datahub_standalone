#!/bin/bash
# stop-compose-containers.sh

set -e

# 动态获取当前路径并设置 docker-compose 文件路径
COMPOSE_FILE="$(pwd)/docker-compose.yml"

# 停止通过 docker-compose 管理的容器
stop_compose_containers() {
  echo "正在停止通过 docker-compose 管理的容器..."
  if [ -f "$COMPOSE_FILE" ]; then
    docker compose -f "$COMPOSE_FILE" stop
    echo "通过 docker-compose 管理的容器已停止。"
  else
    echo "错误：未找到 docker-compose.yml 文件，请确保路径正确。"
    exit 1
  fi
}

# 强制停止未通过 docker-compose 管理的容器
force_stop_non_compose_containers() {
  echo "强制停止未通过 docker-compose 管理的容器..."
  
  # 获取所有运行中的容器 ID 和名称，排除非docker-compose管理的容器
  for container in $(docker ps --filter "status=running" --format "{{.ID}} {{.Names}}"); do
    container_id=$(echo $container | awk '{print $1}')
    container_name=$(echo $container | awk '{print $2}')

    # 仅停止 docker-compose 管理的容器
    if [[ "$container_name" =~ ^datahub ]]; then
      # 确保容器存在并停止
      if docker ps --format "{{.ID}}" | grep -q "$container_id"; then
        echo "停止容器 $container_name (ID: $container_id)..."
        docker stop "$container_id"
      else
        echo "容器 $container_name (ID: $container_id) 已不存在，跳过停止。"
      fi
    else
      echo "跳过容器 $container_name (ID: $container_id) — 不属于 docker-compose 管理。"
    fi
  done
  echo "强制停止非 docker-compose 容器操作完成。"
}

# 执行停止操作
stop_compose_containers
force_stop_non_compose_containers

