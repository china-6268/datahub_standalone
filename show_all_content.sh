#!/bin/bash

# 设置目标目录列表
DIRS=("datahub" "data-init")

# 检查每个目录是否存在
for TARGET_DIR in "${DIRS[@]}"; do
  if [ ! -d "$TARGET_DIR" ]; then
    echo "目录 $TARGET_DIR 不存在！"
    continue
  fi

  echo "目录 $TARGET_DIR 存在。"

  # 输出目录名
  echo "递归列出目录 $TARGET_DIR 下所有文件及其内容："
  echo "--------------------------------------------------------"

  # 查找并输出文件路径及内容
  find "$TARGET_DIR" -type f -print0 | while IFS= read -r -d '' FILE; do
    if [ -f "$FILE" ]; then
      echo "文件: $FILE"
      echo "----------------------"
      # 输出文件内容，最多第一行
      head -n 1 "$FILE"
      echo "----------------------"
    fi
  done

  echo "--------------------------------------------------------"
done

