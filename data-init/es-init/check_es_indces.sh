curl -u elastic:elastic 'http://localhost:29200/_cat/indices?v'


curl -u elastic:elastic 'http://localhost:29200/_cat/indices?v' | awk 'NR==1 || /^yellow|^green|^red/ {print $1, $2, $3, $6}'

curl -u elastic:elastic 'http://localhost:29200/_cat/indices?v' | awk 'NR==1 || /^yellow|^green|^red/ {print $1,$2, $3, $7}'



# 排序展示
curl -u elastic:elastic 'http://localhost:29200/_cat/indices?v' | \
awk 'NR==1 || /^yellow|^green|^red/ {print $1,$2,$3,$7}' | \
sort -t' ' -k2,2 | \
awk '{if ($2 == ".ds-datahub_usage_event-2025.01.15-000001") {print $0} }' && \
curl -u elastic:elastic 'http://47.121.112.172:39828/_cat/indices?v' | \
awk 'NR==1 || /^yellow|^green|^red/ {print $1,$2,$3,$7}' | \
sort -t' ' -k2,2 | \
awk '{if ($2 != ".ds-datahub_usage_event-2025.01.15-000001") {print $0} }'
