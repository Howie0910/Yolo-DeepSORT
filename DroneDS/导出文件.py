import os
import shutil

def organize_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'images')
    train_dir = os.path.join(images_dir, 'val')
    labels_base_dir = os.path.join(base_dir, 'labels')
    labels_train_dir = os.path.join(labels_base_dir, 'val')

    if not os.path.exists(labels_train_dir):
        os.makedirs(labels_train_dir)

    for subfolder in os.listdir(train_dir):
        subfolder_path = os.path.join(train_dir, subfolder)

        if os.path.isdir(subfolder_path):
            print(f"Processing folder: {subfolder_path}")

            for item in os.listdir(subfolder_path):
                item_path = os.path.join(subfolder_path, item)

                if item.lower().endswith(('.jpg')):
                    dest_image_path = os.path.join(train_dir, item)
                    shutil.move(item_path, dest_image_path)
                    print(f"Moved image file: {item} to {train_dir}")

                elif item.lower() == 'labels' and os.path.isdir(item_path):
                    for label_file in os.listdir(item_path):
                        if label_file.lower().endswith('.txt'):
                            src_label_file = os.path.join(item_path, label_file)
                            dest_label_file = os.path.join(labels_train_dir, label_file)
                            shutil.move(src_label_file, dest_label_file)
                            print(f"Moved label file: {label_file} to {labels_train_dir}")

            if not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)
                print(f"Deleted empty folder: {subfolder_path}")

    print("File reorganization completed.")

if __name__ == '__main__':
    organize_files()
