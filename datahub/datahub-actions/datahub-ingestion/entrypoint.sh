#!/bin/bash
set -e

# 创建虚拟环境
python3 -m venv /datahub-ingestion/.venv

# 激活虚拟环境
source /datahub-ingestion/.venv/bin/activate

# 升级 pip 并降级至 <24.1 以避免 nbclient 元数据问题
pip install --upgrade pip -i https://pypi.org/simple/
#pip install --upgrade "pip<24.1" -i https://pypi.org/simple/

# 安装指定的依赖（使用官方 PyPI 镜像）
pip install --no-cache-dir -r /datahub-ingestion/requirements.txt -i https://pypi.org/simple/
pip install --no-cache-dir -r /datahub-ingestion/requirements-actions.txt -i https://pypi.org/simple/

# 启动 DataHub Actions 服务
/datahub-ingestion/.venv/bin/datahub actions run -c /config/actions.yml || echo "DataHub Actions 启动失败，继续保持容器运行"

# 保持容器运行状态，防止退出
tail -f /dev/null

