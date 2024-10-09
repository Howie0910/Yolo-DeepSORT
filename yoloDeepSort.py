import cv2
import json
import os
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

base_path = 'DroneDS\\images\\test'
model = YOLO("yolov8_drone.pt")
tracker = DeepSort(max_age=30, n_init=2, nn_budget=70)# 初始化DeepSORT跟踪器

for folder_name in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder_name)
    if not os.path.isdir(folder_path):
        continue

    json_file_path = os.path.join(folder_path, 'IR_label.json')
    output_json_file = os.path.join(folder_path, f'{folder_name}.json')
    with open(json_file_path, 'r') as f:
        annotations = json.load(f)

    # 提取初始标注框
    initial_frame = annotations["res"][0]
    x_min, y_min, w, h = initial_frame
    x_center = x_min + w / 2
    y_center = y_min + h / 2
    initial_frame_bbox = [int(x_center), int(y_center), w, h]
    # 将第一帧标注框记录到输出结果中
    output_annotations = {"res": [initial_frame_bbox]}
    first_frame_image = os.path.join(folder_path, "000001.jpg")
    image = cv2.imread(first_frame_image)
    detections = model.predict(image, conf=0.5)
    detections_list = []

    for result in detections:
        boxes = result.boxes.xywh.cpu().numpy()  # 获取x, y, w, h
        confidences = result.boxes.conf.cpu().numpy()  # 获取置信度
        classes = result.boxes.cls.cpu().numpy()  # 获取分类标签

        # 将每个目标转换为deepsort格式
        for box, conf, cls in zip(boxes, confidences, classes):
            x, y, w, h = box
            detections_list.append(([x, y, w, h], conf, str(int(cls))))

    tracked_objects = tracker.update_tracks(detections_list, frame=image)

    # 从第二帧开始逐帧检测和跟踪
    frame_index = 2
    while True:
        frame_file = f"{frame_index:06d}.jpg"
        frame_path = os.path.join(folder_path, frame_file)
        if not os.path.exists(frame_path):
            break

        frame_image = cv2.imread(frame_path)
        if frame_image is None:
            break

        # YOLO目标检测
        results = model.predict(frame_image, conf=0.5)
        detections_list = []
        for result in results:
            boxes = result.boxes.xywh.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()

            # 将每个目标转换为deepsort格式
            for box, conf, cls in zip(boxes, confidences, classes):
                x, y, w, h = box
                detections_list.append(([x, y, w, h], conf, str(int(cls))))

        # 目标跟踪
        tracked_objects = tracker.update_tracks(detections_list, frame=frame_image)
        # 如果有跟踪目标，选择置信度最高的标注框
        if len(tracked_objects) > 0:
            valid_tracked_objects = [obj for obj in tracked_objects if obj.det_conf is not None]

            # 如果存在有效目标，选择置信度最高的目标
            if len(valid_tracked_objects) > 0:
                highest_conf_object = max(valid_tracked_objects, key=lambda x: x.det_conf)  # 使用 det_conf 作为置信度
                x, y, w, h = highest_conf_object.to_ltwh()  # 获取目标的边界框（left, top, width, height）
                output_annotations["res"].append([int(x), int(y), int(w), int(h)])  # 转换为 [x, y, w, h] 格式
            else:
                output_annotations["res"].append([])
        else:
            # 如果没有目标，则记录一个空列表
            output_annotations["res"].append([])

        frame_index += 1

    # 输出时，将 [x_center, y_center, w, h] 转换成 [x_min, y_min, w, h]
    for i in range(len(output_annotations["res"])):
        if output_annotations["res"][i]:
            x_center, y_center, w, h = output_annotations["res"][i]
            x_min = x_center - w / 2
            y_min = y_center - h / 2
            output_annotations["res"][i] = [int(x_min), int(y_min), w, h]

    # 保存结果到当前文件夹的输出JSON文件中
    with open(output_json_file, 'w') as f:
        json.dump(output_annotations, f)