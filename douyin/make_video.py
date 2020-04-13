#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/13
    Description:
"""
import os, sys

sys.path.append(os.path.abspath("../common"))
from common import utils_image, utils_io_folder
from tqdm import tqdm

if __name__ == '__main__':
    image_folder_base = "/media/jion/D/chenhaoming/DataSet/DouYin/images/hyj/{}"
    outvid_path_base = "/media/jion/D/chenhaoming/DataSet/DouYin/videos/hyj/{}.mp4"
    list = ["000001", "000002"]
    for item in tqdm(list):
        image_folder = image_folder_base.format(item)
        outvid_path = outvid_path_base.format(item)
        images_paths = utils_io_folder.get_immediate_childfile_paths(image_folder, ext="jpg")
        utils_image.make_video_from_images(images_paths, outvid_path)
