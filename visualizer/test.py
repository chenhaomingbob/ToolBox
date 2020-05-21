#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/28
    Description:
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
joint_names = ['right ankle', 'right knee', 'right pelvis', 'left pelvis',
               'left knee', 'left ankle', 'right wrist',
               'right elbow', 'right shoulder', 'left shoulder', 'left elbow', 'left wrist',
               'upper neck', 'nose', 'head']
joint_pairs = [['head', 'nose', 'purple'],
               ['nose', 'upper neck', 'purple'],
               ['upper neck', 'right shoulder', 'yellow'],
               ['upper neck', 'left shoulder', 'yellow'],
               ['right shoulder', 'right elbow', 'blue'],
               ['right elbow', 'right wrist', 'green'],
               ['left shoulder', 'left elbow', 'blue'],
               ['left elbow', 'left wrist', 'green'],
               ['right shoulder', 'right pelvis', 'yellow'],
               ['left shoulder', 'left pelvis', 'yellow'],
               ['right pelvis', 'right knee', 'red'],
               ['right knee', 'right ankle', 'skyblue'],
               ['left pelvis', 'left knee', 'red'],
               ['left knee', 'left ankle', 'skyblue']]

pose_keypoints_number = len(joint_names)


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


def line_shape(track_id, label, keypoint1, keypoint2):
    shape = dict()
    shape["label"] = label
    shape["points"] = [[float(keypoint1[0]), float(keypoint1[1])], [float(keypoint2[0]), float(keypoint2[1])]]
    shape["group_id"] = track_id
    shape["shape_type"] = "line"
    shape["flags"] = {}
    return shape


def parseArgs():
    parser = argparse.ArgumentParser(description="Convert PoseTrack format to label me format")
    parser.add_argument("-ij", "--input_json", required=False, type=str, default=None,
                        help="")
    parser.add_argument("-iip", "--input_images_dir", required=False, type=str, default=None,
                        help="")
    parser.add_argument("-op", "--output_dir", required=False, type=str, default=None,
                        help="")
    return parser.parse_args()


def posetrack2017_convert_labelme_format(input_json, input_image_path_base, output_dir_base):
    """
    输入是一段视频的json 仅一个json文件，输出为每个帧的json文件
    :param input_json:
    :param input_image_path_base:
    :param output_dir_base:
    :return:
    """
    annolist = utils_json.read_json_from_file(input_json)["annolist"]
    for annotation in annolist:
        # 处理一张图片
        # openPose_object = OpenPose_JSON(input_json)
        input_image_path = os.path.join(input_image_path_base, annotation["image"][0]["name"])
        labelme_object = Labelme_JSON()
        image_name = utils_io_folder.get_file_name_from_path(input_image_path)  # like 00000001.jpg
        labelme_object.imagePath = input_image_path
        labelme_object.imageData = utils_image.img_encode_to_base64(labelme_object.imagePath)
        image_arr = utils_image.img_b64_to_arr(labelme_object.imageData)
        labelme_object.imageHeight, labelme_object.imageWidth = image_arr.shape[0], image_arr.shape[1]
        people = annotation["annorect"]
        for person in people:
            track_id = person["track_id"]
            annopoints = person["annopoints"][0]["point"]
            for point in annopoints:
                point_id = point["id"][0]
                x = point["x"][0]
                y = point["y"][0]
                is_visible = point["is_visible"][0]
                keypoint = [x, y]
                labelme_object.shapes.append(
                    point_shape(track_id, joint_names[point_id] + "_vis_{}".format(is_visible), keypoint))
            for point_1 in annopoints:
                point_1_id = point_1["id"][0]
                x_1 = point_1["x"][0]
                y_1 = point_1["y"][0]
                for point_2 in annopoints:
                    point_2_id = point_2["id"][0]
                    x_2 = point_2["x"][0]
                    y_2 = point_2["y"][0]
                    for joint_pair in joint_pairs:
                        point_1_name = joint_names[point_1_id]
                        point_2_name = joint_names[point_2_id]
                        if joint_pair[0] == point_1_name and joint_pair[1] == point_2_name:
                            labelme_object.shapes.append(
                                line_shape(track_id, point_1_name + point_2_name, [x_1, y_1], [x_2, y_2]))

            path = annotation["image"][0]["name"]
            output_dir = output_dir_base + path[path.index("/"):path.rindex("/")]
            utils_io_folder.create_folder(output_dir)
            output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
            utils_json.write_json_to_file(labelme_object.to_dict(), output_path)


if __name__ == '__main__':
    args = parseArgs()
    test = True
    if test:
        args.input_json = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/val_json/source/000342_mpii.json"
        args.images_path_base = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/posetrack_data"
        args.output_dir_base = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/val_json/labelme"
        posetrack2017_convert_labelme_format(args.input_json, args.images_path_base, args.output_dir_base)
    else:
        # images_paths = utils_io_folder.get_immediate_childfile_paths(args.images_path, exclude=".json")
        intput_jsons = utils_io_folder.get_immediate_childfile_paths(os.path.join(args.input_json), ext=".json")
        # assert len(images_paths) == len(intput_jsons)
        # for index in tqdm(range(len(intput_jsons))):
        #     posetrack2017_convert_labelme_format(intput_jsons[index], images_paths[index], args.output_dir)
        # print(images_paths)
        # print(intpus_jsons)
        # input_jsons = ""
        # input_image_path
        # openpose_convert_labelme_format(args.input_json, args.input_images_dir, args.output_dir)
