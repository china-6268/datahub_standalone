#!/bin/bash

# 设置目标目录列表
DIRS=("datahub" "data-init")

# 初始化文件计数器
TOTAL_FILES=0

# 检查每个目录是否存在
for TARGET_DIR in "${DIRS[@]}"; do
  if [ ! -d "$TARGET_DIR" ]; then
    echo "目录 $TARGET_DIR 不存在！"
    continue
  fi

  # 使用 find 命令统计文件数量
  FILE_COUNT=$(find "$TARGET_DIR" -type f | wc -l)
  echo "目录 $TARGET_DIR 中的文件数量: $FILE_COUNT"

  # 累加到总文件数
  TOTAL_FILES=$((TOTAL_FILES + FILE_COUNT))
done

# 输出所有目录总文件数
echo "所有目录总文件数量: $TOTAL_FILES"

