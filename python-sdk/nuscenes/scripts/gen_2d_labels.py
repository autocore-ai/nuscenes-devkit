import os
import subprocess
def get_subdirectory_names(root_dir):
    """
    获取指定目录下的所有子目录名称。

    :param root_dir: 根目录路径
    :return: 子目录名称列表
    """
    subdirectory_names = []
    try:
        with os.scandir(root_dir) as it:
            for entry in it:
                if entry.is_dir():
                    subdirectory_names.append(entry.name)
    except FileNotFoundError:
        print(f"目录 {root_dir} 不存在")
    except PermissionError:
        print(f"没有权限访问目录 {root_dir}")
    except Exception as e:
        print(f"发生错误: {e}")
    
    return subdirectory_names

def main():
    rootdir = "/home/adas/dataset/Odaiba_JT_v1.0"
    subdirectory_names = get_subdirectory_names(rootdir)
    for subdir_name in subdirectory_names:   
             
        cmd = 'python3 export_2d_annotations_as_json.py  --version {}/annotation --dataroot /home/adas/dataset/Odaiba_JT_v1.0'.format(subdir_name)

        print(cmd)

        # 使用 subprocess.run 执行命令
        try:
            result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
            print(f"Command executed successfully for {subdir_name}:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Command failed for {subdir_name}:")
            print(e.stderr)

if __name__ == "__main__":
    main()