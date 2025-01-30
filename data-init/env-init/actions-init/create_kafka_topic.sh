docker exec -it verify_3-broker-1 kafka-topics --create --topic MetadataChangeLog_Versioned_v1 --bootstrap-server broker:29092 --replication-factor 1 --partitions 1
