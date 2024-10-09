import os
import json

base_dir = os.path.join(os.getcwd(), 'images', 'test')
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)

    if os.path.isdir(folder_path):
        json_file_path = os.path.join(folder_path, f"{folder_name}.json")

        data = {
            "folder_name": folder_name,
            "path": folder_path
        }

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"Created JSON file: {json_file_path}")
