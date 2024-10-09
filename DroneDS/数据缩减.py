import os


def remove_files_except_first(dir_path):
    if not os.path.exists(dir_path):
        print(f"路径不存在: {dir_path}")
        return

    files = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])

    for index, filename in enumerate(files):
        if index % 5 != 0:
            file_path = os.path.join(dir_path, filename)
            os.remove(file_path)
            print(f"删除文件: {file_path}")


def process_image_folder_only(base_folder):
    folder_path = os.path.join(base_folder, "images")
    for sub_folder in ["train", "val"]:
        sub_folder_path = os.path.join(folder_path, sub_folder)
        print(f"正在处理文件夹: {sub_folder_path}")
        remove_files_except_first(sub_folder_path)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    process_image_folder_only(base_dir)
