#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/01
    Description:
"""
import os, sys

sys.path.append(os.path.abspath(r"../../"))
import common.utils_image, common.utils_io_folder
from tqdm import tqdm
from douyin.batch.config import video_types


def video_to_image(video_paths, outimages_paths):
    for video_index in tqdm(range(len(video_paths))):
        video_path = video_paths[video_index]
        outimages_path = outimages_paths[video_index]
        common.utils_image.make_images_from_video(video_path=video_path, outimages_path=outimages_path)
        common.utils_io_folder.create_folder(os.path.join(outimages_path, "openpose"))
        print("id:{},video_to_images Done!".format(video_path))


def start_2060(type):
    assert type in video_types
    video_folder_base = "/media/D/DataSet/DouYin/videos/{}".format(type)
    video_paths = common.utils_io_folder.get_immediate_childfile_paths(video_folder_base, ext="mp4")
    images_folder_base = "/media/D/DataSet/DouYin/images/{}".format(type)
    out_images_paths = []
    for video_path in video_paths:
        video_name = common.utils_io_folder.get_file_name_without_ext_from_path(video_path)
        out_images_paths.append(os.path.join(images_folder_base, video_name))
    video_to_image(video_paths, out_images_paths)


def start(type):
    assert type in video_types
    video_folder_base = "/media/jion/D/chenhaoming/DataSet/DouYin/videos/{}".format(type)
    video_paths = common.utils_io_folder.get_immediate_childfile_paths(video_folder_base, ext="mp4")
    images_folder_base = "/media/jion/D/chenhaoming//DataSet/DouYin/images/{}".format(type)
    out_images_paths = []
    for video_path in video_paths:
        video_name = common.utils_io_folder.get_file_name_without_ext_from_path(video_path)
        out_images_paths.append(os.path.join(images_folder_base, video_name))
    video_to_image(video_paths, out_images_paths)


if __name__ == '__main__':
    # start_2060("KongFu")
    start("KongFu")
