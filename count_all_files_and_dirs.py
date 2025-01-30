import os

def count_files_and_dirs(directory, extensions):
    """
    统计包括当前目录在内的文件夹数量和特定扩展名文件数量

    :param directory: 要统计的根目录
    :param extensions: 文件扩展名列表
    :return: 文件夹数量和每个扩展名对应的文件数量
    """
    file_counts = {ext: 0 for ext in extensions}
    folder_count = 0

    # 检查当前目录是否为文件夹
    if os.path.isdir(directory):
        folder_count += 1  # 当前目录也算一个文件夹

    # 遍历所有子目录和文件
    for root, dirs, files in os.walk(directory):
        folder_count += len(dirs)  # 统计子目录数量
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    file_counts[ext] += 1

    return folder_count, file_counts

if __name__ == "__main__":
    # 设置要统计的目录和扩展名
    target_directory = "/mnt/ssd_nvme3_data/project_root/focusight_zt/verify_3/demo"
    file_extensions = [".sh", ".yml", ".conf", ".properties", ".py", ".sql", ".txt", ".options"]

    # 统计文件夹和文件数量
    folder_count, file_results = count_files_and_dirs(target_directory, file_extensions)

    # 打印统计结果
    print(f"文件夹总数: {folder_count}\n")
    print("各类文件统计:")
    for ext, count in file_results.items():
        print(f"后缀为 {ext} 的文件总数: {count} 个")

