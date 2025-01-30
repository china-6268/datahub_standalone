#!/bin/bash
# run-start-actions.sh

set -e

# 动态获取当前路径并设置 docker-compose 文件路径
COMPOSE_FILE="$(pwd)/docker-compose.yml"

# 记录脚本开始时间
start_time=$(date +%s)

# 启动 datahub-actions 容器
start_actions_container() {
  echo "正在启动 datahub-actions 容器..."
  if [ -f "$COMPOSE_FILE" ]; then

    docker compose -f "$COMPOSE_FILE" start datahub-actions
    #docker compose -f "$COMPOSE_FILE" up -d --no-deps datahub-actions   #这句话丢数据
    echo "datahub-actions 容器已启动。"
  else
    echo "错误：未找到 docker-compose.yml 文件，请确保路径正确。"
    exit 1
  fi
}

# 执行容器启动函数
start_actions_container

# 记录脚本结束时间
end_time=$(date +%s)

# 计算总耗时（单位：秒）
elapsed_time=$((end_time - start_time))

# 输出总耗时
echo "脚本执行总耗时: ${elapsed_time} 秒"

