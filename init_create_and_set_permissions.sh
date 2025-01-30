#!/bin/bash
# 创建目录及赋予权限的脚本（带计时功能）

# 记录脚本开始时间
START_TIME=$(date +%s)

# 获取当前路径
CURRENT_PATH=$(pwd)

# 获取当前用户和组
USER=$(whoami)
GROUP=$(id -gn)

# 定义目录列表
DIRS=(
    "$CURRENT_PATH/datahub/broker/data"
    "$CURRENT_PATH/datahub/broker/etc_kafka"
    "$CURRENT_PATH/datahub/broker/logs"
    "$CURRENT_PATH/datahub/elasticsearch/data"
    "$CURRENT_PATH/datahub/elasticsearch/config"
    "$CURRENT_PATH/datahub/elasticsearch/logs"
    "$CURRENT_PATH/datahub/elasticsearch/tmp"
    "$CURRENT_PATH/datahub/mysql/mysql_data"
    "$CURRENT_PATH/datahub/mysql/logs"
    "$CURRENT_PATH/datahub/mysql/tmp"
    "$CURRENT_PATH/datahub/mysql/mysql_logs"
    "$CURRENT_PATH/datahub/zookeeper/data"
    "$CURRENT_PATH/datahub/zookeeper/log"
    "$CURRENT_PATH/datahub/datahub-actions/config"
    "$CURRENT_PATH/datahub/datahub-actions/data"
    "$CURRENT_PATH/datahub/datahub-actions/datahub-ingestion/.cache"
    "$CURRENT_PATH/datahub/datahub-actions/logs"
    "$CURRENT_PATH/datahub/datahub-actions/tmp/datahub/logs"
    "$CURRENT_PATH/datahub/datahub-actions/tmp/datahub/logs/actions"
    "$CURRENT_PATH/datahub/datahub-actions/etc_datahub_actions_conf"
    "$CURRENT_PATH/datahub/datahub-actions/actions_logs"
    "$CURRENT_PATH/datahub/datahub-actions/datahub_logs"
    "$CURRENT_PATH/datahub/datahub-actions/datahub-ingestion"
    "$CURRENT_PATH/datahub/datahub-actions/datahub-ingestion/.venv"
    "$CURRENT_PATH/datahub/datahub-actions/datahub-ingestion/miniconda"
    "$CURRENT_PATH/datahub/jupyter"
    "$CURRENT_PATH/datahub/datahub-frontend-react/config"
    "$CURRENT_PATH/datahub/datahub-frontend-react/logs"
    "$CURRENT_PATH/datahub/datahub-gms/config"
    "$CURRENT_PATH/datahub/datahub-gms/gms"
    "$CURRENT_PATH/datahub/datahub-gms/data"
    "$CURRENT_PATH/datahub/datahub-gms/logs"
    "$CURRENT_PATH/datahub/datahub-gms/tmp"
    "$CURRENT_PATH/datahub/neo4j/data"
    "$CURRENT_PATH/datahub/neo4j/logs"
    "$CURRENT_PATH/datahub/neo4j/import"
    "$CURRENT_PATH/datahub/neo4j/plugins"
)

# 创建目录并赋予权限
for DIR in "${DIRS[@]}"; do
    STEP_START=$(date +%s)
    
    if [ ! -d "$DIR" ]; then
        echo "正在创建目录: $DIR"
        sudo mkdir -p "$DIR"
    else
        echo "目录已存在: $DIR"
    fi

    # 设置权限为 777
    echo "设置权限为 777: $DIR"
    sudo chmod -R 777 "$DIR"

    # 修改为当前用户和组
    echo "修改目录拥有者为 $USER:$GROUP: $DIR"
    sudo chown -R "$USER":"$GROUP" "$DIR"

    STEP_END=$(date +%s)
    echo "处理 $DIR 耗时: $((STEP_END - STEP_START)) 秒"
done

# 特别处理 datahub-actions 下的日志路径
LOGS_PATH="$CURRENT_PATH/datahub/datahub-actions/logs"
echo "为适配路径设置权限与用户: $LOGS_PATH"
sudo chown -R "$USER":"$GROUP" "$LOGS_PATH"
sudo chmod -R 777 "$LOGS_PATH"

# 确保所有子目录的权限和拥有者设置正确
echo "递归设置所有子目录的权限和拥有者..."
FINAL_STEP_START=$(date +%s)
find "$CURRENT_PATH/datahub" -type d -exec sudo chown -R "$USER":"$GROUP" {} \;
find "$CURRENT_PATH/datahub" -type d -exec sudo chmod -R 777 {} \;
FINAL_STEP_END=$(date +%s)
echo "递归处理耗时: $((FINAL_STEP_END - FINAL_STEP_START)) 秒"

# 记录脚本结束时间并计算总耗时
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
echo "目录创建及权限设置完成，总耗时: $TOTAL_TIME 秒"

