#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/10
    Description:
"""
import sys, os

sys.path.append(os.path.abspath("../common"))
import os
from tqdm import tqdm
from common import utils_image, utils_bbox, utils_json, utils_io_folder
import copy

pose_keypoints_order = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder ankle", "LElbow",
                        "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye",
                        "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"
                        ]
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
    temp_shape = []
    for shape in shapes:
        person_id = shape["group_id"]
        if person_id == 0:
            temp_shape.append(shape)
    output_path = os.path.join(output_folder, utils_io_folder.get_file_name_from_path(labelme_json_path))
    labelme_data["shapes"] = temp_shape
    print(output_path)
    utils_json.write_json_to_file(labelme_data, output_path)


def start_convert():
    labelme_base_path = "F:/DataSet/douyin/my_works/{}"
    index = ["000003"]
    for i in tqdm(index):
        path = labelme_base_path.format(i)
        print(path)
        labelme_json_paths = utils_io_folder.get_immediate_childfile_paths(path, ext="json")
        # TODO  之后要改成在统一的一个目录下
        output_folder = "F:/DataSet/douyin/my_works/{}".format(i)
        utils_io_folder.create_folder(output_folder)
        for labelme_json_path in tqdm(labelme_json_paths):
            number = int(utils_io_folder.get_file_name_without_ext_from_path(labelme_json_path))
            labelme_to_openpose(labelme_json_path, output_folder)


if __name__ == '__main__':
    start_convert()
