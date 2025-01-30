import time
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import MetadataChangeEventClass, DatasetSnapshotClass, UpstreamLineageClass, UpstreamClass
from tqdm import tqdm

# 配置 DataHub REST API
start_time_1 = time.time()
emitter = DatahubRestEmitter("http://localhost:28080")
end_time_1 = time.time()
print(f"配置 DataHub REST API 耗时: {end_time_1 - start_time_1} 秒")

# 定义下游表
start_time_2 = time.time()
downstream_table = make_dataset_urn(platform="mysql", name="datahub.arrayexpress_idf", env="PROD")
end_time_2 = time.time()
print(f"定义下游表 耗时: {end_time_2 - start_time_2} 秒")

# 定义中游表
start_time_3 = time.time()
midstream_table = make_dataset_urn(platform="mysql", name="datahub.disco_sample", env="PROD")
end_time_3 = time.time()
print(f"定义中游表 耗时: {end_time_3 - start_time_3} 秒")

# 定义上游表
start_time_4 = time.time()
upstream_table = make_dataset_urn(platform="mysql", name="datahub.geo_c_serie", env="PROD")
end_time_4 = time.time()
print(f"定义上游表 耗时: {end_time_4 - start_time_4} 秒")

# 创建血缘信息
start_time_5 = time.time()
upstreams = [
    UpstreamClass(dataset=midstream_table, type="TRANSFORMED"),
]
middle_lineage = UpstreamLineageClass(upstreams=upstreams)

upstreams = [
    UpstreamClass(dataset=upstream_table, type="TRANSFORMED"),
]
final_lineage = UpstreamLineageClass(upstreams=upstreams)
end_time_5 = time.time()
print(f"创建血缘信息 耗时: {end_time_5 - start_time_5} 秒")

# 创建 Snapshot
start_time_6 = time.time()
mid_snapshot = DatasetSnapshotClass(urn=midstream_table, aspects=[middle_lineage])
final_snapshot = DatasetSnapshotClass(urn=downstream_table, aspects=[final_lineage])
end_time_6 = time.time()
print(f"创建 Snapshot 耗时: {end_time_6 - start_time_6} 秒")

# 创建 Metadata Change Event (MCE)
start_time_7 = time.time()
mid_mce = MetadataChangeEventClass(proposedSnapshot=mid_snapshot)
final_mce = MetadataChangeEventClass(proposedSnapshot=final_snapshot)
end_time_7 = time.time()
print(f"创建 Metadata Change Event (MCE) 耗时: {end_time_7 - start_time_7} 秒")

# 提交到 DataHub
start_time_8 = time.time()
with tqdm(total=100, desc="提交中游关系到 DataHub") as pbar:
    emitter.emit_mce(mid_mce)
    pbar.update(100)
with tqdm(total=100, desc="提交最终关系到 DataHub") as pbar:
    emitter.emit_mce(final_mce)
    pbar.update(100)
end_time_8 = time.time()
print(f"提交到 DataHub 耗时: {end_time_8 - start_time_8} 秒")

print("geo_c_serie -> disco_sample -> arrayexpress_idf 的血缘关系已成功提交")

