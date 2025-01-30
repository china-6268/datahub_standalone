#!/bin/bash
# download-docker-images.sh
set -e

# 镜像列表（从 docker-compose.yml 中提取）
IMAGES=(
    "neo4j:4.4"
    "confluentinc/cp-kafka:7.4.0"
    "acryldata/datahub-actions:head"
    "acryldata/datahub-frontend-react:head"
    "acryldata/datahub-gms:head"
    "acryldata/datahub-upgrade:head"
    "elasticsearch:7.10.1"
    "acryldata/datahub-elasticsearch-setup:head"
    "acryldata/datahub-kafka-setup:head"
    "mysql:8.2"
    "acryldata/datahub-mysql-setup:head"
    "confluentinc/cp-schema-registry:7.4.0"
    "confluentinc/cp-zookeeper:7.4.0"
)

# 拉取镜像
echo "开始下载镜像..."
for IMAGE in "${IMAGES[@]}"; do
    echo "下载镜像: $IMAGE"
    docker pull "$IMAGE"
done

echo "所有镜像下载完成。"

