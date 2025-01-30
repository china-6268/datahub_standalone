import re
import sys
import os

def update_yaml(input_file, output_file, new_first_digit):
    """
    将输入文件中的所有5位数数字的万位数字替换为new_first_digit，
    并将结果写入输出文件。
    
    :param input_file: 输入YAML文件路径。
    :param output_file: 输出YAML文件路径。
    :param new_first_digit: 用于替换的万位数字（单个数字字符）。
    """
    # 确保new_first_digit是单个数字
    if not (new_first_digit.isdigit() and len(new_first_digit) == 1):
        print("错误: new_first_digit必须是单个数字（0-9）。")
        sys.exit(1)
    
    # 编译正则表达式，匹配精确的5位数数字
    # (?<!\d)确保前面不是数字，避免匹配更长数字中的部分
    # (?!\d)确保后面不是数字，避免匹配更长数字中的部分
    pattern = re.compile(r'(?<!\d)(\d)(\d{4})(?!\d)')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
            infile.seek(0)  # 重置文件指针到开头
            
            for i, line in enumerate(infile, 1):
                # 使用lambda函数动态替换万位数字
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

def main():
    """
    主函数，处理命令行参数并调用update_yaml函数。
    """
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python generate_env.py <new_digit>0000")
        print("示例: python generate_env.py 40000")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # 验证输入参数是5位数
    if not (input_arg.isdigit() and len(input_arg) == 5):
        print("错误: 参数必须是5位数，例如 40000")
        sys.exit(1)
    
    new_first_digit = input_arg[0]
    
    input_file = './docker-compose.yml'
    output_file = './docker-compose_updated.yml'
    
    # 检查输入文件是否存在
    if not os.path.isfile(input_file):
        print(f"错误: 输入文件 '{input_file}' 不存在。")
        sys.exit(1)
    
    update_yaml(input_file, output_file, new_first_digit)

if __name__ == "__main__":
    main()

