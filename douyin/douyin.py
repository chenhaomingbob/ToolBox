#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/01
    Description:
"""

import utils_image
import utils_io_folder
from tqdm import tqdm
import os

import utils_io_folder


def video_to_image(video_paths, outimages_paths):
    for video_index in tqdm(range(len(video_paths))):
        video_path = video_paths[video_index]
        outimages_path = outimages_paths[video_index]
        utils_image.make_images_from_video(video_path=video_path, outimages_path=outimages_path)
        utils_io_folder.create_folder(os.path.join(outimages_path, "openpose"))
        print("id:{},video_to_images Done!".format(video_path))


if __name__ == '__main__':
    # video_paths = ["/media/jion/D/chenhaoming/DataSet/DouYin/Data/dance_3_Abily/_a_1.mp4"]
    # outimages_paths = ["/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/_a_1"]
    video_paths = []
    outimages_paths = []
    video_base = "/media/jion/D/chenhaoming/DataSet/DouYin/Data/dance_3_Abily/{0:06d}.mp4"
    outimages_path = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/"
    for i in range(1, 37):
        video_paths.append(os.path.join(video_base).format(i))
        outimages_paths.append(os.path.join(outimages_path).format(i))

    video_to_image(video_paths, outimages_paths)
    # cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/_a_1 --write_json /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/_a_1 --hand"
    # os.system(cmd)
