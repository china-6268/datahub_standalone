#!/usr/bin/bash
set -e  # 遇到错误立即退出
set -x  # 打印每条执行的命令（调试用）

echo "Activating virtual environment..."
source /datahub-ingestion/.venv/bin/activate

if [ -n "$ACTIONS_EXTRA_PACKAGES" ]; then
  echo "Installing extra packages: $ACTIONS_EXTRA_PACKAGES"
  pip install $ACTIONS_EXTRA_PACKAGES
fi

if [[ -n "$ACTIONS_CONFIG" && -n "$ACTIONS_EXTRA_PACKAGES" ]]; then
  mkdir -p /tmp/datahub/logs
  curl -q "$ACTIONS_CONFIG" -o config.yaml
  exec dockerize -wait ${DATAHUB_GMS_PROTOCOL:-http}://$DATAHUB_GMS_HOST:$DATAHUB_GMS_PORT/health -timeout 240s \
    datahub actions --config config.yaml
else
  exec datahub "$@"
fi

