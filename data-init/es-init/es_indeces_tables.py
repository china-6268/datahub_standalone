import subprocess

def fetch_index_data(url):
    # 获取 Elasticsearch 索引数据
    curl_cmd = f"curl -u elastic:elastic '{url}/_cat/indices?v' | \
                 awk 'NR==1 || /^yellow|^green|^red/ {{print $1,$2,$3,$7}}' | \
                 sort -t' ' -k2,2"
    result = subprocess.check_output(curl_cmd, shell=True, text=True)
    return result

def process_index_data(index_data):
    # 处理索引数据，将其拆分成列
    rows = index_data.splitlines()
    filtered_data = []
    for row in rows:
        cols = row.split()
        if cols and len(cols) >= 4:
            # 区分出特定的索引，如 ".ds-datahub_usage_event-2025.01.15-000001"
            if cols[1] == ".ds-datahub_usage_event-2025.01.15-000001":
                filtered_data.append(cols)
            else:
                filtered_data.append(cols)
    return filtered_data

def print_table(filtered_data):
    # 打印数据表格
    print(f"{'序号':<5} {'索引名称':<50} {'文档数'}")
    print("-" * 80)
    for idx, row in enumerate(filtered_data, 1):
        print(f"{idx:<5} {row[1]:<50} {row[3]}")

# Elasticsearch 服务器 URL
url = "http://47.121.112.172:39828"

# 获取并处理数据
index_data = fetch_index_data(url)
filtered_data = process_index_data(index_data)
print_table(filtered_data)

