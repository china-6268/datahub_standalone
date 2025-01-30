import time
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import MetadataChangeEventClass, DatasetSnapshotClass, UpstreamLineageClass, UpstreamClass
from tqdm import tqdm

# 配置 DataHub REST API
start_time_1 = time.time()
emitter = DatahubRestEmitter("http://localhost:28080")  # 替换为实际 DataHub GMS 地址
end_time_1 = time.time()
print(f"配置 DataHub REST API 耗时: {end_time_1 - start_time_1} 秒")

# 定义下游表
start_time_2 = time.time()
downstream_tables = [
    make_dataset_urn(platform="mysql", name="geo_e_characteristic", env="PROD"),
    make_dataset_urn(platform="mysql", name="geo_e_description", env="PROD")
]
end_time_2 = time.time()
print(f"定义下游表 耗时: {end_time_2 - start_time_2} 秒")

# 定义上游表
start_time_3 = time.time()
upstream_table = make_dataset_urn(platform="mysql", name="geo_c_sample", env="PROD")
end_time_3 = time.time()
print(f"定义上游表 耗时: {end_time_3 - start_time_3} 秒")

# 创建血缘信息并提交每个下游表的血缘关系
for downstream_table in downstream_tables:
    # 创建血缘信息
    start_time_4 = time.time()
    upstreams = [UpstreamClass(dataset=upstream_table, type="TRANSFORMED")]
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
    with tqdm(total=100, desc=f"提交到 DataHub: {downstream_table}") as pbar:
        emitter.emit_mce(mce)
        pbar.update(100)
    end_time_7 = time.time()
    print(f"提交到 DataHub 耗时: {end_time_7 - start_time_7} 秒")

print("所有血缘信息已成功提交")

