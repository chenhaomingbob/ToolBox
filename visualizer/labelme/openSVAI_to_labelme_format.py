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
import json as JSON
from common import utils_image, utils_bbox, utils_json, utils_io_folder

from data_format.openSVAI import OpenSVAI_JSON
from data_format.labelme import Labelme_JSON
import argparse

# openSVAI  keypoints order (same as PoseTrack)
# 0-right ankle 1-right knee ....
keypoints_order = ["right_ankle", "right_knee", "right_hip", "left_hip", "left_knee", "left ankle", "right_wrist",
                   "right_elbow", "right_shoulder", "left_shoulder", "left_elbow", "left_wrist", "head_bottom", "nose",
                   "head_top"]
keypoints_number = len(keypoints_order)


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
    shape["points"] = [[keypoint[0], keypoint[1]]]
    shape["group_id"] = track_id
    shape["shape_type"] = "point"
    shape["flags"] = {}
    return shape


def parseArgs():
    parser = argparse.ArgumentParser(description="Convert OpenSVAI format to label me format")
    parser.add_argument("-ij", "--input_json", required=True, type=str, default=None,
                        help="")
    parser.add_argument("-iip", "--input_images_dir", required=False, type=str, default=None,
                        help="")
    parser.add_argument("-op", "--output_dir", required=False, type=str, default=None,
                        help="")
    return parser.parse_args()


def openSVAI_convert_labelme_format(input_json, input_images_dir=None, output_dir=None):
    openSVAI_object = OpenSVAI_JSON(input_json)

    for frame in openSVAI_object.frames:
        labelme_object = Labelme_JSON()
        image_info = frame["image"]
        candidates_info = frame["candidates"]
        image_name = image_info["name"]  # like 00000001.jpg
        if input_images_dir is None:
            labelme_object.imagePath = os.path.join(image_info["folder"], image_info["name"])
        else:
            labelme_object.imagePath = os.path.join(input_images_dir, image_name)
        labelme_object.imageData = utils_image.img_encode_to_base64(labelme_object.imagePath)
        image_arr = utils_image.img_b64_to_arr(labelme_object.imageData)
        labelme_object.imageHeight, labelme_object.imageWidth = image_arr.shape[0], image_arr.shape[1]
        for candidate in candidates_info:
            track_id = candidate['track_id']  # 对应 labelme的group_id
            det_bbox = candidate["det_bbox"]
            # det_bbox (open_SVAI) - rectangle (labelme)
            labelme_object.shapes.append(rectangle_shape(track_id, det_bbox))
            keypoints = numpy.array(candidate['pose_keypoints_2d']).reshape(-1, 3)
            for index, keypoint in enumerate(keypoints):
                # keypoint (open_SVAI) - point (labelme)
                labelme_object.shapes.append(point_shape(track_id, keypoints_order[index], keypoint))
        if output_dir is None:
            # 输出 默认在input_json的路径下创建labelme文件夹。
            output_dir = os.path.join(utils_io_folder.get_parent_folder_from_path(input_json), "labelme")
            utils_io_folder.create_folder(output_dir)
            output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
        else:
            utils_io_folder.create_folder(output_dir)
            output_path = os.path.join(output_dir, utils_io_folder.replace_file_ext(image_name, "json"))
        utils_json.write_json_to_file(labelme_object.to_dict(), output_path)


if __name__ == '__main__':
    args = parseArgs()
    print(args)
    test = True
    if test:
        args.input_json = "E:/111/experiment/come/2017-iou-1.5-pose-0-interval-3/jsons/023653_mpii.json"
        args.input_images_dir = "C:/Users/chenh/Desktop/023653_mpii"
        args.output_dir = "C:/Users/chenh/Desktop/023653_mpii/labelme"
    openSVAI_convert_labelme_format(args.input_json, args.input_images_dir, args.output_dir)
