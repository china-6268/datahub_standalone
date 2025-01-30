import re
import sys
import os

def update_docker_compose(input_file, output_file, new_first_digit):
    """
    修改 docker-compose.yml 文件中的5位数端口号的万位数字。
    
    :param input_file: 输入的 docker-compose.yml 文件路径。
    :param output_file: 输出的 docker-compose_updated.yml 文件路径。
    :param new_first_digit: 新的万位数字（字符串形式的单个数字）。
    """
    # 确保 new_first_digit 是单个数字
    if not (new_first_digit.isdigit() and len(new_first_digit) == 1):
        print("错误: new_first_digit 必须是单个数字（0-9）。")
        sys.exit(1)
    
    # 编译正则表达式，匹配精确的5位数数字
    # (?<!\d) 确保前面不是数字，避免匹配更长数字中的部分
    # (?!\d) 确保后面不是数字，避免匹配更长数字中的部分
    pattern = re.compile(r'(?<!\d)(\d)(\d{4})(?!\d)')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            # 计算总行数以便显示进度
            total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
            infile.seek(0)  # 重置文件指针到开头
            
            for i, line in enumerate(infile, 1):
                # 使用 lambda 函数动态替换万位数字
                updated_line = pattern.sub(lambda m: f'{new_first_digit}{m.group(2)}', line)
                outfile.write(updated_line)
                
                # 打印处理进度
                if i % 100 == 0 or i == total_lines:
                    print(f"处理进度：{i}/{total_lines} 行")
        
        print(f"修改后的文件已保存为 '{output_file}'")
    
    except FileNotFoundError:
        print(f"错误: 文件 '{input_file}' 未找到。")
        sys.exit(1)
    except IOError as e:
        print(f"文件读写错误: {e}")
        sys.exit(1)

def generate_env_file(env_file_path, base_port):
    """
    根据基准端口生成 .env 文件。
    
    :param env_file_path: 生成的 .env 文件路径。
    :param base_port: 基准端口（整数）。
    """
    try:
        base_port_int = int(base_port)
        if not (10000 <= base_port_int <= 99999):
            print("错误: 基准端口必须是5位数。")
            sys.exit(1)
    except ValueError:
        print("错误: 基准端口必须是一个整数。")
        sys.exit(1)
    
    # 定义各个服务的端口偏移量
    port_offsets = {
        "DATAHUB_MAPPED_NEO4J_HTTP_PORT": 7474,
        "DATAHUB_MAPPED_NEO4J_BOLT_PORT": 7687,
        "DATAHUB_MAPPED_KAFKA_BROKER_PORT": 9092,
        "DATAHUB_MAPPED_SCHEMA_REGISTRY_PORT": 8081,
        "DATAHUB_MAPPED_FRONTEND_PORT": 9002,
        "DATAHUB_MAPPED_GMS_PORT": 8080,
        "DATAHUB_MAPPED_ELASTIC_PORT": 9200,
        "DATAHUB_MAPPED_MYSQL_PORT": 3306,
        "DATAHUB_MAPPED_ZK_PORT": 2181
    }
    
    try:
        with open(env_file_path, 'w', encoding='utf-8') as env_file:
            env_file.write("# Base port (万位)\n")
            env_file.write(f"BASE_PORT={base_port_int}\n\n")
            
            env_file.write("# DataHub version\n")
            env_file.write("# DATAHUB_VERSION=0.14.1\n\n")
            
            # 生成各个服务的端口
            env_file.write("# NEO4j\n")
            env_file.write(f"DATAHUB_MAPPED_NEO4J_HTTP_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_NEO4J_HTTP_PORT']}\n")
            env_file.write(f"DATAHUB_MAPPED_NEO4J_BOLT_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_NEO4J_BOLT_PORT']}\n\n")
            
            env_file.write("# Kafka Broker\n")
            env_file.write(f"DATAHUB_MAPPED_KAFKA_BROKER_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_KAFKA_BROKER_PORT']}\n\n")
            
            env_file.write("# Schema Registry\n")
            env_file.write(f"DATAHUB_MAPPED_SCHEMA_REGISTRY_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_SCHEMA_REGISTRY_PORT']}\n\n")
            
            env_file.write("# DataHub Frontend\n")
            env_file.write(f"DATAHUB_MAPPED_FRONTEND_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_FRONTEND_PORT']}\n\n")
            
            env_file.write("# DataHub GMS\n")
            env_file.write(f"DATAHUB_MAPPED_GMS_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_GMS_PORT']}\n")
            env_file.write("#  # 启用身份认证\n")
            env_file.write("METADATA_SERVICE_AUTH_ENABLED=true\n\n")
            
            env_file.write("# Elasticsearch\n")
            env_file.write(f"DATAHUB_MAPPED_ELASTIC_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_ELASTIC_PORT']}\n\n")
            
            env_file.write("# MySQL\n")
            env_file.write(f"DATAHUB_MAPPED_MYSQL_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_MYSQL_PORT']}\n\n")
            
            env_file.write("# Zookeeper\n")
            env_file.write(f"DATAHUB_MAPPED_ZK_PORT={base_port_int + port_offsets['DATAHUB_MAPPED_ZK_PORT']}\n")
        
        print(f".env 文件已生成，基准端口为 {base_port_int}")
    
    except IOError as e:
        print(f"文件写入错误: {e}")
        sys.exit(1)

def main():
    """
    主函数，处理命令行参数并调用相应的功能。
    """
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python generate_env.py <base_port>")
        print("示例: python generate_env.py 40000")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # 验证输入参数是5位数
    if not (input_arg.isdigit() and len(input_arg) == 5):
        print("错误: 参数必须是5位数，例如 40000")
        sys.exit(1)
    
    base_port = input_arg
    new_first_digit = base_port[0]
    
    input_docker_compose = './docker-compose.yml'
    output_docker_compose = './docker-compose_updated.yml'
    env_file_path = './.env'
    
    # 检查输入文件是否存在
    if not os.path.isfile(input_docker_compose):
        print(f"错误: 输入文件 '{input_docker_compose}' 不存在。")
        sys.exit(1)
    
    # 更新 docker-compose.yml 文件
    update_docker_compose(input_docker_compose, output_docker_compose, new_first_digit)
    
    # 生成 .env 文件
    generate_env_file(env_file_path, base_port)

if __name__ == "__main__":
    main()

