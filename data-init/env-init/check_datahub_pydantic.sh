#!/bin/bash

# 输出当前 Python 版本
echo "Python version:"
python --version

# 输出当前激活的 Conda 环境名称
echo "Active Conda environment:"
conda env list | grep '*' | awk '{print $1}'

# 检查 datahub 和 pydantic 相关包
echo "Installed datahub and pydantic packages:"
python -m pip freeze | grep -E "datahub|pydantic"

