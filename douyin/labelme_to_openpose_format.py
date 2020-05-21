#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/05
    Description: 将labelme格式转换为openpose格式
"""
import os, sys

sys.path.append(os.path.abspath("../common"))
from common import utils_io_folder, utils_json
from batch.config import video_types
from tqdm import tqdm

pose_keypoints_order = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow",
                        "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye",
                        "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"]
hand_keypoints_order = ["{}hand_keypoint_0", "{}hand_keypoint_1", "{}hand_keypoint_2",
                        "{}hand_keypoint_3", "{}hand_keypoint_4", "{}hand_keypoint_5",
                        "{}hand_keypoint_6", "{}hand_keypoint_7", "{}hand_keypoint_8",
                        "{}hand_keypoint_9", "{}hand_keypoint_10", "{}hand_keypoint_11",
                        "{}hand_keypoint_12", "{}hand_keypoint_13", "{}hand_keypoint_14",
                        "{}hand_keypoint_15", "{}hand_keypoint_16", "{}hand_keypoint_17",
                        "{}hand_keypoint_18", "{}hand_keypoint_19", "{}hand_keypoint_20", ]
hand_type = ["left_", "right_"]
left_hand_keypoints_order = [keypoint.format(hand_type[0]) for keypoint in hand_keypoints_order]
right_hand_keypoints_order = [keypoint.format(hand_type[1]) for keypoint in hand_keypoints_order]
openpose_hand_keypoints_number = 21


# 一次转换一个json文件
def labelme_to_openpose(labelme_json_path, output_folder):
    labelme_data = utils_json.read_json_from_file(labelme_json_path)
    img_name = utils_io_folder.get_file_name_without_ext_from_path(labelme_json_path)
    shapes = labelme_data["shapes"]
    # for shape in shapes:
    openpose_data = dict()
    person_dicts = dict()
    person_ids = []
    next_id = 0
    for shape in shapes:
        person_id = shape["group_id"]
        if person_id not in person_ids:
            person_dict = dict()
            if person_id != -1:
                person_dict["person_id"] = person_id
            else:
                person_dict["person_id"] = next_id
                next_id += 1
            person_dict["pose_keypoints_2d"] = [0] * (len(pose_keypoints_order) * 3)
            person_dict["face_keypoints_2d"] = []
            person_dict["hand_left_keypoints_2d"] = [0] * (openpose_hand_keypoints_number * 3)
            person_dict["hand_right_keypoints_2d"] = [0] * (openpose_hand_keypoints_number * 3)
            person_dict["pose_keypoints_3d"] = []
            person_dict["face_keypoints_3d"] = []
            person_dict["hand_right_keypoints_3d"] = []
            person_dict = fill_keypoint(person_dict, shape)
            person_dicts[person_id] = person_dict
            person_ids.append(person_id)
        else:
            person_dict = person_dicts[person_id]
            person_dict = fill_keypoint(person_dict, shape)
            person_dicts[person_id] = person_dict
    output_path = os.path.join(output_folder, utils_io_folder.get_file_name_from_path(labelme_json_path))
    python_data = dict()
    python_data["version"] = 1.3
    people = []
    for person_index in person_dicts.keys():
        people.append(person_dicts[person_index])
    python_data["people"] = people
    utils_json.write_json_to_file(python_data, output_path)


def fill_keypoint(person_dict, shape):
    label = shape["label"]
    points = shape["points"][0]
    shape_type = shape["shape_type"]

    if label in pose_keypoints_order:
        label_index = pose_keypoints_order.index(label) * 3
        if point_valid(points):
            person_dict["pose_keypoints_2d"][label_index] = points[0]
            person_dict["pose_keypoints_2d"][label_index + 1] = points[1]
            person_dict["pose_keypoints_2d"][label_index + 2] = 1
    elif label in left_hand_keypoints_order:
        label_index = int(label[label.rindex("_") + 1:]) * 3
        if point_valid(points):
            person_dict["hand_left_keypoints_2d"][label_index] = points[0]
            person_dict["hand_left_keypoints_2d"][label_index + 1] = points[1]
            person_dict["hand_left_keypoints_2d"][label_index + 2] = 1
    elif label in right_hand_keypoints_order:
        label_index = int(label[label.rindex("_") + 1:]) * 3
        if point_valid(points):
            person_dict["hand_right_keypoints_2d"][label_index] = points[0]
            person_dict["hand_right_keypoints_2d"][label_index + 1] = points[1]
            person_dict["hand_right_keypoints_2d"][label_index + 2] = 1
    elif label == "LShoulder ankle":
        label_index = 5 * 3
        if point_valid(points):
            person_dict["pose_keypoints_2d"][label_index] = points[0]
            person_dict["pose_keypoints_2d"][label_index + 1] = points[1]
            person_dict["pose_keypoints_2d"][label_index + 2] = 1
    return person_dict


def point_valid(points):
    assert len(points) == 2
    if points[0] < 1 and points[1] < 1:
        return False
    return True


def start_convert():
    labelme_base_path = "F:/DataSet/DouYin/annotation_labelme_image/{}"
    output_base_path = "F:/DataSet/DouYin/annotation_openpose/{}"
    for video_type in tqdm(video_types):
        openpose_json_folder_type = output_base_path.format(video_type)
        labelme_folder = labelme_base_path.format(video_type)

        video_folder_sequence = utils_io_folder.get_immediate_subfolder_paths(labelme_folder)
        for video_folder in tqdm(video_folder_sequence):
            folder_name = utils_io_folder.get_file_name_without_ext_from_path(video_folder)
            if folder_name.isdigit():
                openpose_json_folder = os.path.join(openpose_json_folder_type, folder_name)
                utils_io_folder.create_folder(openpose_json_folder)
                labelme_json_paths = utils_io_folder.get_immediate_childfile_paths(video_folder, ext="json")
                for labelme_json_path in tqdm(labelme_json_paths):
                    # convert json one by one
                    labelme_to_openpose(labelme_json_path, openpose_json_folder)


if __name__ == '__main__':
    start_convert()
