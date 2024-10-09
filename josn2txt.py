import os
import json

folder_path = 'result_yolo+DeepSort'

if not os.path.exists(folder_path):
    print(f"文件夹 {folder_path} 不存在。")
    exit()

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        json_file_path = os.path.join(folder_path, filename)

        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"无法解析 {filename}，错误: {e}")
                continue

        txt_filename = filename.replace('.json', '.txt')
        txt_file_path = os.path.join(folder_path, txt_filename)
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            for key, value in data.items():
                txt_file.write(f"{key}: {value}\n")
