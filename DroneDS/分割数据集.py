import os
import random
import shutil

def split_folders():
    base_dir = os.getcwd()
    images_dir = os.path.join(base_dir, 'images')
    train_dir = os.path.join(images_dir, 'train')
    val_dir = os.path.join(images_dir, 'val')

    if not os.path.exists(train_dir):
        print(f"Error: {train_dir} not found.")
        return

    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    subfolders = [subfolder for subfolder in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, subfolder))]

    random.shuffle(subfolders)

    train_split = int(0.8 * len(subfolders))
    val_subfolders = subfolders[train_split:]

    for subfolder in val_subfolders:
        src_folder = os.path.join(train_dir, subfolder)
        dest_folder = os.path.join(val_dir, subfolder)
        shutil.move(src_folder, dest_folder)
        print(f"Moved folder: {subfolder} to {val_dir}")

    print("Folder Train/Val split completed.")

if __name__ == '__main__':
    split_folders()
