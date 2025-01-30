#!/bin/bash

# 打印 actions.yml 配置文件的内容
echo "====持久化映射到宿主机的容器内actions.yml ===="
cat ./datahub/datahub-actions/config/actions.yml

# 打印 requirements.txt 文件的内容
#echo "==== requirements.txt ===="
#cat ./datahub/datahub-actions/datahub-ingestion/requirements.txt

# 打印 requirements-actions.txt 文件的内容
#echo "==== requirements-actions.txt ===="
#cat ./datahub/datahub-actions/datahub-ingestion/requirements-actions.txt

# 打印 requirements-jupyter.txt 文件的内容
#echo "==== requirements-jupyter.txt ===="
#cat ./datahub/datahub-actions/datahub-ingestion/requirements-jupyter.txt

# 打印 entrypoint.sh 脚本的内容
#echo "==== entrypoint.sh ===="
#cat ./datahub/datahub-actions/datahub-ingestion/entrypoint.sh

# 打印 docker-compose.yml 文件的第 38 到第 134 行
# 该部分被注释掉，如果需要查看部分内容，可以取消注释
#echo "==== docker-compose.yml (lines 38-134) ===="
#head -n 97 docker-compose.yml | tail -n 37

# 打印 docker-compose.yml 文件的第 61 到第 111 行（可调整行数范围）
echo "==== docker-compose.yml  中 actions 容器yml部分 (head -n 120 docker-compose.yml| tail -n 60) ===="
#head -n 111 docker-compose.yml | tail -n 51
head -n 120 docker-compose.yml| tail -n 60
echo "==== docker-compose.yml 全部内容) ===="
cat docker-compose.yml

# 列出当前正在运行的 Docker 容器的名称和端口信息
echo "==== Docker Containers (Names and Ports) ===="
sudo docker ps --format "table {{.Names}}\t{{.Ports}}"

# 打印 JupyterLab 容器的最近 20 行日志
#echo "==== JupyterLab Logs 最近 20 行日志 ===="
#sudo docker logs --tail 20 verify_2-jupyterlab-1

# 打印 DataHub Actions 容器的最近 20 行日志
echo "==== DataHub Actions Logs 最近 100 行日志===="
sudo docker logs --tail 100 verify_3-datahub-actions-1

# 进入 MySQL 容器并以 datahub 用户身份连接到 MySQL
#echo "==== Enter MySQL inside the container (datahub user) ===="
#sudo docker exec -u root -it verify_2-mysql-1 mysql -u datahub -p

# 查看 宿主机 datahub版本 
#echo "====  宿主机 datahub 版本===="
#datahub version
echo "====  actions 容器 Dockerfile 的内容 ===="
cat ./data-init/env-init/actions-init/Dockerfile_actions-v0.1.6
