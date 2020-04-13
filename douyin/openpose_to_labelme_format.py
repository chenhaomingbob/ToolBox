#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/23
    Description: OpenSVAI format convert to labelme format
"""
import os
import sys

sys.path.append(os.path.abspath("../common"))
import numpy
import json
from common import utils_image, utils_bbox, utils_json, utils_io_folder

from data_format.openpose import OpenPose_JSON
from data_format.labelme import Labelme_JSON
import argparse
from tqdm import tqdm
from batch.config import video_types

# openSVAI  keypoints order (same as PoseTrack)
# 0-right ankle 1-right knee ....
pose_keypoints_order = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow",
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
hand_keep_point = [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20]
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
    labelme_object.imagePath = ""
    # labelme_object.imageData = ""
    labelme_object.imageData = utils_image.img_encode_to_base64(input_image_path)
    image_arr = utils_image.img_b64_to_arr(utils_image.img_encode_to_base64(input_image_path))
    labelme_object.imageHeight, labelme_object.imageWidth = image_arr.shape[0], image_arr.shape[1]

    for person in openPose_object.people:
        track_id = person["person_id"]
        pose_keypoints_2d = person["pose_keypoints_2d"]
        hand_left_keypoints_2d = person["hand_left_keypoints_2d"]
        hand_right_keypoints_2d = person["hand_right_keypoints_2d"]
        for index, keypoint in enumerate(pose_keypoints_2d):
            labelme_object.shapes.append(point_shape(track_id, pose_keypoints_order[index], keypoint))
        for index, keypoint in enumerate(hand_left_keypoints_2d):
            if index in hand_keep_point:
                labelme_object.shapes.append(
                    point_shape(track_id, hand_keypoints_order[index].format("left_"), keypoint))
        for index, keypoint in enumerate(hand_right_keypoints_2d):
            if index in hand_keep_point:
                labelme_object.shapes.append(
                    point_shape(track_id, hand_keypoints_order[index].format("right_"), keypoint))
    if output_dir is None:
        # 输出 默认在input_json的路径下创建labelme文件夹。
        output_dir = os.path.join(utils_io_folder.get_parent_folder_from_path(input_json))
        # utils_io_folder.create_folder(output_dir)
        output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
    else:
        utils_io_folder.create_folder(output_dir)
        output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
    utils_json.write_json_to_file(labelme_object.to_dict(), output_path)


def generate_one_video(video_id, type=None):
    args.images_path = "F:/DataSet/douyin/images/dance/{0:06d}".format(video_id)
    args.output_dir = "F:/DataSet/douyin/trial/dance/{0:06d}".format(video_id)
    args.openpose_dir = "F:/DataSet/douyin/openpose/dance/{0:06d}".format(video_id)
    images_paths = utils_io_folder.get_immediate_childfile_paths(args.images_path, exclude=".json")
    input_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(args.openpose_dir), ext=".json")
    assert len(images_paths) == len(input_jsons)
    print("args.images_path:{}".format(args.images_path))
    for index in range(len(images_paths)):
        openpose_convert_labelme_format(input_jsons[index], images_paths[index], args.output_dir)


def generate_all_video(type):
    assert type in video_types
    "machine_openpose"
    "/media/jion/D/chenhaoming/DataSet/DouYin/machine_openpose/KongFu/000001"
    image_folder_base = "/media/jion/D/chenhaoming/DataSet/DouYin/images/{}".format(type)
    openpose_dir_base = "/media/jion/D/chenhaoming/DataSet/DouYin/machine_openpose/{}".format(type)
    output_dir_base = "/media/jion/D/chenhaoming/DataSet/DouYin/images/{}".format(type)

    images_folder_paths = utils_io_folder.get_immediate_subfolder_paths(image_folder_base)
    for image_folder_path in images_folder_paths:
        images_paths = utils_io_folder.get_immediate_childfile_paths(image_folder_path, exclude=".json")
        video_name = utils_io_folder.get_file_name_without_ext_from_path(image_folder_path)
        input_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(openpose_dir_base, video_name),
                                                                    ext=".json")
        output_dir = os.path.join(output_dir_base, video_name)
        assert len(images_paths) == len(input_jsons)
        print("images_path:{}".format(image_folder_path))
        for index in range(len(images_paths)):
            openpose_convert_labelme_format(input_jsons[index], images_paths[index], output_dir)
    # if type == "dance":
    #     #     for video_id in tqdm(range(1, 36)):
    #     #         args.images_path = "F:/DataSet/douyin/images/dance/{0:06d}".format(video_id)
    #     #         args.output_dir = "F:/DataSet/douyin/trial/dance/{0:06d}".format(video_id)
    #     #         args.openpose_dir = "F:/DataSet/douyin/openpose/dance/{0:06d}".format(video_id)
    #     #         if not utils_io_folder.folder_exists(args.images_path):
    #     #             continue
    #     #         images_paths = utils_io_folder.get_immediate_childfile_paths(args.images_path, exclude=".json")
    #     #         input_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(args.openpose_dir), ext=".json")
    #     #         assert len(images_paths) == len(input_jsons)
    #     #         print("args.images_path:{}".format(args.images_path))
    #     #         for index in range(len(images_paths)):
    #     #             openpose_convert_labelme_format(input_jsons[index], images_paths[index], args.output_dir)
    #     # elif type == "fitness":
    #     #     for video_id in tqdm(range(1, 8)):
    #     #         args.images_path = "/media/jion/D/chenhaoming/DataSet/DouYin/images/fitness/{0:06d}".format(video_id)
    #     #         args.openpose_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/openpose_json/fitness/{0:06d}".format(
    #     #             video_id)
    #     #         args.output_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/fitness/{0:06d}".format(video_id)
    #     #         if not utils_io_folder.folder_exists(args.images_path):
    #     #             continue
    #     #         images_paths = utils_io_folder.get_immediate_childfile_paths(args.images_path, exclude=".json")
    #     #         input_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(args.openpose_dir), ext=".json")
    #     #         assert len(images_paths) == len(input_jsons)
    #     #         print("args.images_path:{}".format(args.images_path))
    #     #         for index in range(len(images_paths)):
    #     #             openpose_convert_labelme_format(input_jsons[index], images_paths[index], args.output_dir)


# def generate_all_video():
#     platforms = ["ubuntu", "windows"]
#     platform = platforms[1]
#     for i in tqdm(range(1, 36)):
#         if platform == "ubuntu":
#             args.images_path = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}".format(i)
#             args.output_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}".format(i)
#
#         else:
#             args.images_path = "F:/DataSet/douyin/images/dance/{0:06d}".format(i)
#             args.output_dir = "F:/DataSet/douyin/images/dance/{0:06d}".format(i)
#             args.openpose_dir = "F:/DataSet/douyin/openpose/dance/{0:06d}".format(i)
#         if not utils_io_folder.folder_exists(args.images_path):
#             continue
#         images_paths = utils_io_folder.get_immediate_childfile_paths(args.images_path, exclude=".json")
#         input_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(args.openpose_dir), ext=".json")
#         assert len(images_paths) == len(input_jsons)
#         print("args.images_path:{}".format(args.images_path))
#         for index in range(len(images_paths)):
#             openpose_convert_labelme_format(input_jsons[index], images_paths[index], args.output_dir)


if __name__ == '__main__':
    args = parseArgs()
    # generate_all_video("fitness")
    generate_all_video("hyj")
    # test_one_video(16)
