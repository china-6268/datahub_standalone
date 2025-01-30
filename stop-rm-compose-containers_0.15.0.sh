#!/bin/bash
# stop-rm-compose-containers.sh

set -e

# 动态获取当前路径并设置 docker-compose 文件路径
COMPOSE_FILE="$(pwd)/docker-compose.yml"

# 停止并删除通过 docker-compose 管理的容器
stop_compose_containers() {
  echo "正在停止并删除通过 docker-compose 管理的容器..."
  if [ -f "$COMPOSE_FILE" ]; then
    docker compose -f "$COMPOSE_FILE" down --remove-orphans
    echo "通过 docker-compose 管理的容器已停止并删除。"
  else
    echo "错误：未找到 docker-compose.yml 文件，请确保路径正确。"
    exit 1
  fi
}

# 强制停止并删除未通过 docker-compose 管理的容器
force_stop_and_remove_non_compose_containers() {
  echo "强制停止并删除未通过 docker-compose 管理的容器..."
  
  # 获取所有退出的容器 ID 和名称，排除掉非docker-compose管理的容器
  for container in $(docker ps -a --filter "status=exited" --format "{{.ID}} {{.Names}}"); do
    container_id=$(echo $container | awk '{print $1}')
    container_name=$(echo $container | awk '{print $2}')
    
    # 仅删除 docker-compose 管理的容器
    if [[ "$container_name" =~ ^datahub ]]; then
      # 确保容器存在并删除
      if docker ps -a --format "{{.ID}}" | grep -q "$container_id"; then
        echo "删除容器 $container_name (ID: $container_id)..."
        docker rm -f "$container_id"  # 使用 -f 强制删除
      else
        echo "容器 $container_name (ID: $container_id) 已不存在，跳过删除。"
      fi
    else
      echo "跳过容器 $container_name (ID: $container_id) — 不属于 docker-compose 管理。"
    fi
  done
  echo "强制删除未停止的容器操作完成。"
}

# 删除 datahub_network 网络（如果存在）
remove_datahub_network() {
  echo "正在删除 datahub_network 网络（如果存在）..."
  if docker network ls --filter "name=datahub_network" --format "{{.Name}}" | grep -q "datahub_network"; then
    docker network rm datahub_network
    echo "datahub_network 网络已删除。"
  else
    echo "没有找到 datahub_network 网络，跳过删除。"
  fi
}

# 执行停止并删除操作
stop_compose_containers
force_stop_and_remove_non_compose_containers
remove_datahub_network

