#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六层血缘关系示例：
geo_c_serie -> disco_sample -> arrayexpress_idf -> arrayexpress_sdrf -> embl_ena_sample -> [ gtex_sample, embl_ena_experiment ]
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
    print("开始执行六层血缘脚本...")

    # -------------------------------------------------------------
    # 1. 配置 DataHub REST API
    # -------------------------------------------------------------
    start_time_1 = time.time()
    emitter = DatahubRestEmitter(
            gms_server="http://192.168.150.110:28080",  # GMS 服务地址
            token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6ImY0MWJjZjQ0LTY5ZGMtNGEwNS1iN2U2LTA5ODM5OWYyZDU5MyIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3NDUzMTMzNDcsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.FqbJXEkd6ZgKtOWaXj0XUIBaCho17BQptCfh83aptWM",  # 如果有 token，替换为实际值
            #username="datahub",  # 用户名
            #password="datahub"   # 密码
    )
    end_time_1 = time.time()
    print(f"配置 DataHub REST API 耗时: {end_time_1 - start_time_1:.2f} 秒")

    # -------------------------------------------------------------
    # 2. 定义所有表的 URN
    # -------------------------------------------------------------
    start_time_2 = time.time()
    geo_c_serie_urn = make_dataset_urn(platform="mysql", name="datahub.geo_c_serie", env="PROD")
    disco_sample_urn = make_dataset_urn(platform="mysql", name="datahub.disco_sample", env="PROD")
    arrayexpress_idf_urn = make_dataset_urn(platform="mysql", name="datahub.arrayexpress_idf", env="PROD")
    arrayexpress_sdrf_urn = make_dataset_urn(platform="mysql", name="datahub.arrayexpress_sdrf", env="PROD")
    embl_ena_sample_urn = make_dataset_urn(platform="mysql", name="datahub.embl_ena_sample", env="PROD")
    gtex_sample_urn = make_dataset_urn(platform="mysql", name="datahub.gtex_sample", env="PROD")
    embl_ena_experiment_urn = make_dataset_urn(platform="mysql", name="datahub.embl_ena_experiment", env="PROD")
    end_time_2 = time.time()
    print(f"定义所有表的 URN 耗时: {end_time_2 - start_time_2:.2f} 秒")

    # -------------------------------------------------------------
    # 3. 构建各层血缘信息：每个下游表指向其上游表
    #    1) disco_sample -> geo_c_serie
    #    2) arrayexpress_idf -> disco_sample
    #    3) arrayexpress_sdrf -> arrayexpress_idf
    #    4) embl_ena_sample -> arrayexpress_sdrf
    #    5) gtex_sample -> embl_ena_sample
    #    6) embl_ena_experiment -> embl_ena_sample
    # -------------------------------------------------------------
    start_time_3 = time.time()

    # 中游1: disco_sample 的上游为 geo_c_serie
    disco_sample_upstreams = [UpstreamClass(dataset=geo_c_serie_urn, type="TRANSFORMED")]
    disco_sample_lineage = UpstreamLineageClass(upstreams=disco_sample_upstreams)
    disco_sample_snapshot = DatasetSnapshotClass(
        urn=disco_sample_urn,
        aspects=[disco_sample_lineage]
    )
    disco_sample_mce = MetadataChangeEventClass(proposedSnapshot=disco_sample_snapshot)

    # 中游2: arrayexpress_idf 的上游为 disco_sample
    arrayexpress_idf_upstreams = [UpstreamClass(dataset=disco_sample_urn, type="TRANSFORMED")]
    arrayexpress_idf_lineage = UpstreamLineageClass(upstreams=arrayexpress_idf_upstreams)
    arrayexpress_idf_snapshot = DatasetSnapshotClass(
        urn=arrayexpress_idf_urn,
        aspects=[arrayexpress_idf_lineage]
    )
    arrayexpress_idf_mce = MetadataChangeEventClass(proposedSnapshot=arrayexpress_idf_snapshot)

    # 中游3: arrayexpress_sdrf 的上游为 arrayexpress_idf
    arrayexpress_sdrf_upstreams = [UpstreamClass(dataset=arrayexpress_idf_urn, type="TRANSFORMED")]
    arrayexpress_sdrf_lineage = UpstreamLineageClass(upstreams=arrayexpress_sdrf_upstreams)
    arrayexpress_sdrf_snapshot = DatasetSnapshotClass(
        urn=arrayexpress_sdrf_urn,
        aspects=[arrayexpress_sdrf_lineage]
    )
    arrayexpress_sdrf_mce = MetadataChangeEventClass(proposedSnapshot=arrayexpress_sdrf_snapshot)

    # 中游4: embl_ena_sample 的上游为 arrayexpress_sdrf
    embl_ena_sample_upstreams = [UpstreamClass(dataset=arrayexpress_sdrf_urn, type="TRANSFORMED")]
    embl_ena_sample_lineage = UpstreamLineageClass(upstreams=embl_ena_sample_upstreams)
    embl_ena_sample_snapshot = DatasetSnapshotClass(
        urn=embl_ena_sample_urn,
        aspects=[embl_ena_sample_lineage]
    )
    embl_ena_sample_mce = MetadataChangeEventClass(proposedSnapshot=embl_ena_sample_snapshot)

    # 末层1: gtex_sample 的上游为 embl_ena_sample
    gtex_sample_upstreams = [UpstreamClass(dataset=embl_ena_sample_urn, type="TRANSFORMED")]
    gtex_sample_lineage = UpstreamLineageClass(upstreams=gtex_sample_upstreams)
    gtex_sample_snapshot = DatasetSnapshotClass(
        urn=gtex_sample_urn,
        aspects=[gtex_sample_lineage]
    )
    gtex_sample_mce = MetadataChangeEventClass(proposedSnapshot=gtex_sample_snapshot)

    # 末层2: embl_ena_experiment 的上游为 embl_ena_sample
    embl_ena_experiment_upstreams = [UpstreamClass(dataset=embl_ena_sample_urn, type="TRANSFORMED")]
    embl_ena_experiment_lineage = UpstreamLineageClass(upstreams=embl_ena_experiment_upstreams)
    embl_ena_experiment_snapshot = DatasetSnapshotClass(
        urn=embl_ena_experiment_urn,
        aspects=[embl_ena_experiment_lineage]
    )
    embl_ena_experiment_mce = MetadataChangeEventClass(proposedSnapshot=embl_ena_experiment_snapshot)

    end_time_3 = time.time()
    print(f"构建各层血缘信息 耗时: {end_time_3 - start_time_3:.2f} 秒")

    # -------------------------------------------------------------
    # 4. 提交到 DataHub：分步提交每个 MCE
    # -------------------------------------------------------------
    start_time_4 = time.time()
    with tqdm(total=100, desc="提交六层血缘到 DataHub") as pbar:
        # 提交 disco_sample 血缘
        emitter.emit_mce(disco_sample_mce)
        pbar.update(15)

        # 提交 arrayexpress_idf 血缘
        emitter.emit_mce(arrayexpress_idf_mce)
        pbar.update(15)

        # 提交 arrayexpress_sdrf 血缘
        emitter.emit_mce(arrayexpress_sdrf_mce)
        pbar.update(15)

        # 提交 embl_ena_sample 血缘
        emitter.emit_mce(embl_ena_sample_mce)
        pbar.update(15)

        # 提交 gtex_sample 血缘
        emitter.emit_mce(gtex_sample_mce)
        pbar.update(20)

        # 提交 embl_ena_experiment 血缘
        emitter.emit_mce(embl_ena_experiment_mce)
        pbar.update(20)

    end_time_4 = time.time()
    print(f"提交到 DataHub 耗时: {end_time_4 - start_time_4:.2f} 秒")

    print("geo_c_serie -> disco_sample -> arrayexpress_idf -> arrayexpress_sdrf -> embl_ena_sample -> [gtex_sample, embl_ena_experiment] 六层血缘已全部提交")
    end_time_all = time.time()
    print(f"脚本总耗时: {end_time_all - start_time_all:.2f} 秒")

if __name__ == "__main__":
    main()

