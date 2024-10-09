import os
import shutil

root_dir = os.path.join(os.getcwd(), 'images', 'test')
result_dir = os.path.join(os.getcwd(), 'result')

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        json_file = os.path.join(folder_path, f'{folder}.json')
        if os.path.exists(json_file):
            dest_path = os.path.join(result_dir, f'{folder}.json')
            shutil.move(json_file, dest_path)
            print(f'Moved: {json_file} to {dest_path}')
        else:
            print(f'No matching JSON file found in: {folder_path}')
