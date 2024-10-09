import os
import json


def convert_to_yolo_format(video_dir, img_width, img_height, class_id=0):
    label_file = os.path.join(video_dir, 'IR_label.json')
    if not os.path.exists(label_file):
        print(f"IR_label.json not found in {video_dir}")
        return

    with open(label_file, 'r') as f:
        label_data = json.load(f)

    exist = label_data["exist"]
    gt_rect = label_data["gt_rect"]

    for idx, exist_flag in enumerate(exist):
        img_file = f"{idx + 1:06d}.jpg"
        txt_file = os.path.join(video_dir, 'labels', f"{idx + 1:06d}.txt")

        os.makedirs(os.path.join(video_dir, 'labels'), exist_ok=True)

        if exist_flag == 1 and gt_rect[idx]:
            x, y, w, h = gt_rect[idx]

            x_center = (x + w / 2) / img_width
            y_center = (y + h / 2) / img_height
            width = w / img_width
            height = h / img_height

            with open(txt_file, 'w') as f:
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        else:
            # 如果不存在目标，创建空标签文件
            with open(txt_file, 'w') as f:
                pass

    print(f"Processed labels for {video_dir}")


def process_images_and_labels(base_dir, img_width, img_height):
    if not os.path.exists(base_dir):
        print(f"Base directory '{base_dir}' not found.")
        return

    for video_folder in os.listdir(base_dir):
        video_dir = os.path.join(base_dir, video_folder)
        if not os.path.isdir(video_dir):
            continue

        print(f"Processing video folder: {video_folder}")

        convert_to_yolo_format(video_dir, img_width, img_height)
        rename_files(video_dir, video_folder)


def rename_files(video_dir, video_folder):
    for img_file in os.listdir(video_dir):
        if img_file.endswith('.jpg'):
            old_img_path = os.path.join(video_dir, img_file)
            new_img_name = f"{video_folder}_{img_file}"
            new_img_path = os.path.join(video_dir, new_img_name)
            os.rename(old_img_path, new_img_path)
            print(f"Renamed image: {old_img_path} -> {new_img_path}")

    labels_dir = os.path.join(video_dir, 'labels')
    if os.path.exists(labels_dir):
        for txt_file in os.listdir(labels_dir):
            if txt_file.endswith('.txt'):
                old_txt_path = os.path.join(labels_dir, txt_file)
                new_txt_name = f"{video_folder}_{txt_file}"
                new_txt_path = os.path.join(labels_dir, new_txt_name)
                os.rename(old_txt_path, new_txt_path)
                print(f"Renamed label: {old_txt_path} -> {new_txt_path}")


base_directory = r'D:\Coding\DroneDS\images\train'
image_width = 640
image_height = 512

process_images_and_labels(base_directory, image_width, image_height)
