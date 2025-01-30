基础环境前提:
py=3.10
pip最新版,安装acryl-datahub==0.14.1
pip install 'acryl-datahub[mysql]' 

在action容器内 uv pip install 'acryl-datahub[datahub-rest,datahub-kafka,mysql]==0.14.1' -i https://mirrors.aliyun.com/pypi/simple/

0.先执行初始化脚本
1.不动默认库 datahub 默认表:metadata_aspect_v2
2.ingestion 动作 后web页面才能看到数据 
3. hostname -I 查看 本地 ip 然后绑定  yml
4.blook关系可以预先创建,有了数据就会展示
