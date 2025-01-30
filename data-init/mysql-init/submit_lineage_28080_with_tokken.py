import time
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import MetadataChangeEventClass, DatasetSnapshotClass, UpstreamLineageClass, UpstreamClass
from tqdm import tqdm
from requests.auth import HTTPBasicAuth  # 导入认证模块

# 配置 DataHub REST API
start_time_1 = time.time()

# 如果需要使用基本认证（用户名和密码）：
emitter = DatahubRestEmitter(
    "http://localhost:28080", 
    # auth=HTTPBasicAuth('your_username', 'your_password')  # 替换成实际用户名和密码
     token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6IjJmY2U3MzYyLWFhZmEtNDU1NC1hZDg0LTZhMjhkMWIzMzQ5YiIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3NDQ3OTk0OTMsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.RfHjKj2PQHhrKsAs4HlhJeOBIRQ2UpgZ_hSFMxj4BcM"
)

# 如果是使用 API Token，您可以改为如下：
# emitter = DatahubRestEmitter(
#     "http://localhost:28080", 
#     token="your_api_token"  # 替换成实际的 API Token
# )

end_time_1 = time.time()
print(f"配置 DataHub REST API 耗时: {end_time_1 - start_time_1} 秒")

# 定义下游表
start_time_2 = time.time()
#downstream_table = make_dataset_urn(platform="mysql", name="tpcds.store_sales", env="PROD")
downstream_table = make_dataset_urn(platform="mysql", name="datahub.store_sales", env="PROD")
end_time_2 = time.time()
print(f"定义下游表 耗时: {end_time_2 - start_time_2} 秒")

# 定义上游表
start_time_3 = time.time()
upstream_tables = [
    make_dataset_urn(platform="mysql", name="datahub.customer", env="PROD"),
    make_dataset_urn(platform="mysql", name="datahub.product", env="PROD")
]
end_time_3 = time.time()
print(f"定义上游表 耗时: {end_time_3 - start_time_3} 秒")

# 创建血缘信息
start_time_4 = time.time()
upstreams = [UpstreamClass(dataset=upstream_table, type="TRANSFORMED") for upstream_table in upstream_tables]
lineage = UpstreamLineageClass(upstreams=upstreams)
end_time_4 = time.time()
print(f"创建血缘信息 耗时: {end_time_4 - start_time_4} 秒")

# 创建 Snapshot
start_time_5 = time.time()
snapshot = DatasetSnapshotClass(urn=downstream_table, aspects=[lineage])
end_time_5 = time.time()
print(f"创建 Snapshot 耗时: {end_time_5 - start_time_5} 秒")

# 创建 Metadata Change Event (MCE)
start_time_6 = time.time()
mce = MetadataChangeEventClass(proposedSnapshot=snapshot)
end_time_6 = time.time()
print(f"创建 Metadata Change Event (MCE) 耗时: {end_time_6 - start_time_6} 秒")

# 提交到 DataHub
start_time_7 = time.time()
with tqdm(total=100, desc="推送到 DataHub") as pbar:
    emitter.emit_mce(mce)
    pbar.update(100)
end_time_7 = time.time()
print(f"推送到 DataHub 耗时: {end_time_7 - start_time_7} 秒")

print("血缘信息已成功推送")

