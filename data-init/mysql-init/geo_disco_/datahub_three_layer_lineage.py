#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三层血缘：geo_c_serie -> disco_sample -> arrayexpress_idf
全程耗时输出并带进度条
"""
import time
from tqdm import tqdm
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    MetadataChangeEventClass,
    DatasetSnapshotClass,
    UpstreamLineageClass,
    UpstreamClass
)

def main():
    start_time_all = time.time()
    print("开始执行三层血缘脚本...")
    
    # 配置 DataHub REST API
    start_time_1 = time.time()
    emitter = DatahubRestEmitter("http://localhost:28080")
    end_time_1 = time.time()
    print(f"配置 DataHub REST API 耗时: {end_time_1 - start_time_1:.2f} 秒")

    # 定义数据集 URN
    start_time_2 = time.time()
    geo_c_serie_urn = make_dataset_urn(platform="mysql", name="datahub.geo_c_serie", env="PROD")
    disco_sample_urn = make_dataset_urn(platform="mysql", name="datahub.disco_sample", env="PROD")
    arrayexpress_idf_urn = make_dataset_urn(platform="mysql", name="datahub.arrayexpress_idf", env="PROD")
    end_time_2 = time.time()
    print(f"定义数据集 URN 耗时: {end_time_2 - start_time_2:.2f} 秒")

    # -------------------------
    # Step1: 中游 disco_sample 有上游 geo_c_serie
    # -------------------------
    start_time_3 = time.time()
    mid_upstreams = [UpstreamClass(dataset=geo_c_serie_urn, type="TRANSFORMED")]
    mid_lineage = UpstreamLineageClass(upstreams=mid_upstreams)
    mid_snapshot = DatasetSnapshotClass(
        urn=disco_sample_urn,
        aspects=[mid_lineage]
    )
    mid_mce = MetadataChangeEventClass(proposedSnapshot=mid_snapshot)
    end_time_3 = time.time()
    print(f"构建中游血缘信息 耗时: {end_time_3 - start_time_3:.2f} 秒")

    # -------------------------
    # Step2: 下游 arrayexpress_idf 有上游 disco_sample
    # -------------------------
    start_time_4 = time.time()
    final_upstreams = [UpstreamClass(dataset=disco_sample_urn, type="TRANSFORMED")]
    final_lineage = UpstreamLineageClass(upstreams=final_upstreams)
    final_snapshot = DatasetSnapshotClass(
        urn=arrayexpress_idf_urn,
        aspects=[final_lineage]
    )
    final_mce = MetadataChangeEventClass(proposedSnapshot=final_snapshot)
    end_time_4 = time.time()
    print(f"构建下游血缘信息 耗时: {end_time_4 - start_time_4:.2f} 秒")

    # -------------------------
    # 提交到 DataHub
    # -------------------------
    start_time_5 = time.time()
    with tqdm(total=100, desc="提交三层血缘到 DataHub") as pbar:
        emitter.emit_mce(mid_mce)
        pbar.update(50)
        emitter.emit_mce(final_mce)
        pbar.update(50)
    end_time_5 = time.time()
    print(f"提交到 DataHub 耗时: {end_time_5 - start_time_5:.2f} 秒")

    print("geo_c_serie -> disco_sample -> arrayexpress_idf 三层血缘已成功提交")
    end_time_all = time.time()
    print(f"脚本总耗时: {end_time_all - start_time_all:.2f} 秒")

if __name__ == "__main__":
    main()

