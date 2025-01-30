sink:
    type: datahub-rest
    config:
        server: 'http://172.18.0.7:8080'
source:
    type: mysql
    config:
        host_port: '172.18.0.3:3306'
        database: datahub
        username: datahub
        password: datahub
        schema_pattern:
            allow:
                - '.*'
        table_pattern:
            allow:
                - '.*'
