#!/bin/bash

# 设置目标目录
TARGET_DIR="data-init"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
  echo "目录 $TARGET_DIR 不存在！"
  exit 1
fi

# 输出目录名
echo "递归列出目录 $TARGET_DIR 下所有文件及其内容："
echo "--------------------------------------------------------"

# 递归查找所有文件
find "$TARGET_DIR" -type f | while read -r FILE; do
  echo "文件: $FILE"
  echo "----------------------"
  # 输出文件内容，最多前10行
  head -n 10 "$FILE" 
  echo "----------------------"
done

