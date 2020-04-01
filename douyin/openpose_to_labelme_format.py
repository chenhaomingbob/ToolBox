#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/23
    Description: OpenSVAI format convert to labelme format
"""
import os
import numpy
import json
from common import utils_image, utils_bbox, utils_json, utils_io_folder

from data_format.openpose import OpenPose_JSON
from data_format.labelme import Labelme_JSON
import argparse
from tqdm import tqdm

# openSVAI  keypoints order (same as PoseTrack)
# 0-right ankle 1-right knee ....
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
pose_keypoints_number = len(pose_keypoints_order)
hand_keypoints_number = len(hand_keypoints_order)


def rectangle_shape(track_id, det_bbox):
    if not utils_bbox.bbox_invalid(det_bbox):
        shape = dict()
        x1, y1, x2, y2 = utils_bbox.xywh_to_x1y1x2y2(det_bbox)
        shape["label"] = "person_{}".format(track_id)
        shape["points"] = [[x1, y1], [x2, y2]]
        shape["group_id"] = track_id
        shape["shape_type"] = "rectangle"
        shape["flags"] = {}
        return shape
    else:
        return None


def point_shape(track_id, label, keypoint):
    shape = dict()
    shape["label"] = label
    shape["points"] = [[float(keypoint[0]), float(keypoint[1])]]
    shape["group_id"] = track_id
    shape["shape_type"] = "point"
    shape["flags"] = {}
    return shape


def parseArgs():
    parser = argparse.ArgumentParser(description="Convert OpenSVAI format to label me format")
    parser.add_argument("-ij", "--input_json", required=False, type=str, default=None,
                        help="")
    parser.add_argument("-iip", "--input_images_dir", required=False, type=str, default=None,
                        help="")
    parser.add_argument("-op", "--output_dir", required=False, type=str, default=None,
                        help="")
    return parser.parse_args()


def openpose_convert_labelme_format(input_json, input_image_path=None, output_dir=None):
    openPose_object = OpenPose_JSON(input_json)
    labelme_object = Labelme_JSON()
    image_name = utils_io_folder.get_file_name_from_path(input_image_path)  # like 00000001.jpg
    labelme_object.imagePath = input_image_path
    labelme_object.imageData = utils_image.img_encode_to_base64(labelme_object.imagePath)
    image_arr = utils_image.img_b64_to_arr(labelme_object.imageData)
    labelme_object.imageHeight, labelme_object.imageWidth = image_arr.shape[0], image_arr.shape[1]

    for person in openPose_object.people:
        track_id = person["person_id"]
        pose_keypoints_2d = person["pose_keypoints_2d"]
        hand_left_keypoints_2d = person["hand_left_keypoints_2d"]
        hand_right_keypoints_2d = person["hand_right_keypoints_2d"]
        for index, keypoint in enumerate(pose_keypoints_2d):
            labelme_object.shapes.append(point_shape(track_id, pose_keypoints_order[index], keypoint))
        for index, keypoint in enumerate(hand_left_keypoints_2d):
            labelme_object.shapes.append(point_shape(track_id, hand_keypoints_order[index].format("left_"), keypoint))
        for index, keypoint in enumerate(hand_right_keypoints_2d):
            labelme_object.shapes.append(point_shape(track_id, hand_keypoints_order[index].format("right_"), keypoint))
    if output_dir is None:
        # 输出 默认在input_json的路径下创建labelme文件夹。
        output_dir = os.path.join(utils_io_folder.get_parent_folder_from_path(input_json))
        # utils_io_folder.create_folder(output_dir)
        output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
    else:
        utils_io_folder.create_folder(output_dir)
        output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
    utils_json.write_json_to_file(labelme_object.to_dict(), output_path)


if __name__ == '__main__':
    args = parseArgs()

    for i in tqdm(range(1, 36)):
        args.images_path = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}".format(i)
        args.output_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}".format(i)
        images_paths = utils_io_folder.get_immediate_childfile_paths(args.images_path, exclude=".json")
        intput_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(args.images_path, "openpose"),
                                                                     ext=".json")
        assert len(images_paths) == len(intput_jsons)
        for index in range(len(images_paths)):
            openpose_convert_labelme_format(intput_jsons[index], images_paths[index], args.output_dir)
