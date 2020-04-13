#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/01
    Description:
"""

import os,sys

sys.path.append(os.path.abspath(r"../../"))
# sys.path.append(os.path.abspath(r"../../common"))
import common.utils_io_folder
from douyin.batch.config import video_types


def tem_start(type):
    assert type in video_types
    if type == "dance":
        image_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}"
        write_json_base = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/openpose"
    elif type == "fitness":
        image_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/fitness/{0:06d}"
        write_json_base = "/media/jion/D/chenhaoming/DataSet/DouYin/openpose_json/fitness/{0:06d}"
    else:
        return
    cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir {} --write_json {} --hand"
    des = "/media/jion/D/chenhaoming/Code/openpose"
    os.chdir(des)
    for i in range(1, 8):
        image_dir_i = image_dir.format(i)
        write_json_i = write_json_base.format(i)
        if not os.path.exists(write_json_i):
            os.mkdir(write_json_i)
        os.system(cmd.format(image_dir_i, write_json_i))

def start(type):
    assert type in video_types
    image_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/{}".format(type)
    # write_json_base = "/media/D/DataSet/DouYin/images/{}/{0:06d}/openpose"
    write_json_base = "/media/jion/D/chenhaoming/DataSet/DouYin/machine_openpose/{}".format(type)

    cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir {} --write_json {} --hand"
    des = "/media/jion/D/chenhaoming/Code/openpose"
    os.chdir(des)
    subfolder_paths = common.utils_io_folder.get_immediate_subfolder_paths(image_dir)
    for subfolder_path in subfolder_paths:
        video_name = common.utils_io_folder.get_file_name_without_ext_from_path(subfolder_path)
        write_json = os.path.join(write_json_base, video_name)
        if not os.path.exists(write_json):
            common.utils_io_folder.create_folder(write_json)

        os.system(cmd.format(subfolder_path, write_json))

def tem_start_2060(type):
    assert type in video_types
    image_dir = "/media/D/DataSet/DouYin/images/{}".format(type)
    # write_json_base = "/media/D/DataSet/DouYin/images/{}/{0:06d}/openpose"
    write_json_base = "/media/D/DataSet/DouYin/machine_openpose/{}".format(type)

    cmd = "/media/D/Code/openpose/build/examples/openpose/openpose.bin --image_dir {} --write_json {} --hand"
    des = "/media/D/Code/openpose"
    os.chdir(des)
    subfolder_paths = common.utils_io_folder.get_immediate_subfolder_paths(image_dir)
    for subfolder_path in subfolder_paths:
        video_name = common.utils_io_folder.get_file_name_without_ext_from_path(subfolder_path)
        write_json = os.path.join(write_json_base, video_name)
        if not os.path.exists(write_json):
            common.utils_io_folder.create_folder(write_json)

        os.system(cmd.format(subfolder_path, write_json))





if __name__ == '__main__':
    start("hyj")
    # start("KongFu")
