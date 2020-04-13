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
from douyin.batch.config import video_types
import common.utils_io_folder
from tqdm import tqdm


def zip_images_json(type):
    assert type in video_types
    platforms = ["ubuntu", "windows"]
    platform = platforms[0]
    if platform == "ubuntu":
        des = "/media/jion/D/chenhaoming/DataSet/DouYin/images/{}".format(type)
        cmd = "zip -r {}.zip {}/"
        os.chdir(des)
        sub_folder_paths = common.utils_io_folder.get_immediate_subfolder_names(des)
        for sub_folder_path in sub_folder_paths:
            video_name = common.utils_io_folder.get_file_name_without_ext_from_name(sub_folder_path)
            cmd_i = cmd.format(video_name, video_name)
            print(cmd_i)
            os.system(cmd_i)
    elif platform == "windows":
        des = "F:/DataSet/douyin/images/dance"
        os.chdir(des)
        target_base = "{0:06d}.zip"
        # target_base = "F:/DataSet/douyin/images/dance/{0:06d}.zip"
        source = "{0:06d}"

        zip_command = "zip -r {} {}"
        for i in range(17, 36):
            source_i = source.format(i)
            target_i = target_base.format(i)
            if common.utils_io_folder.folder_exists(source_i):

                zip_command_i = zip_command.format(target_i, source_i)
                print(zip_command_i)
                os.system(zip_command_i)
            else:
                print("{} not exist".format(source_i))


def zip_only_json():
    platforms = ["ubuntu", "windows"]
    platform = platforms[1]
    if platform == "ubuntu":
        # cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d} --write_json /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/openpose --hand"
        des = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance"
        cmd = "zip -r {0:06d}.zip {0:06d}/"
        os.chdir(des)
        for i in range(1, 36):
            os.system(cmd.format(i, i))
    elif platform == "windows":
        des = "F:/DataSet/douyin/trial/dance"
        os.chdir(des)
        target_base = "{0:06d}.zip"
        # target_base = "F:/DataSet/douyin/images/dance/{0:06d}.zip"
        source = "{0:06d}"

        zip_command = "zip -r {} {}"
        for i in range(0, 36):
            source_i = source.format(i)
            target_i = target_base.format(i)
            if utils_io_folder.folder_exists(source_i):

                zip_command_i = zip_command.format(target_i, source_i)
                print(zip_command_i)
                os.system(zip_command_i)
            else:
                print("{} not exist".format(source_i))


def zip_all():
    platforms = ["ubuntu", "windows"]
    platform = platforms[1]
    if platform == "ubuntu":
        # cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d} --write_json /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/openpose --hand"
        des = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance"
        cmd = "zip -r {0:06d}.zip {0:06d}/"
        os.chdir(des)
        for i in range(1, 36):
            os.system(cmd.format(i, i))
    elif platform == "windows":
        des = "F:/DataSet/douyin/images/dance"
        os.chdir(des)
        target_base = "{0:06d}.zip"
        # target_base = "F:/DataSet/douyin/images/dance/{0:06d}.zip"
        source = "{0:06d}"

        zip_command = "zip -r {} {}"
        for i in range(17, 36):
            source_i = source.format(i)
            target_i = target_base.format(i)
            if common.utils_io_folder.folder_exists(source_i):

                zip_command_i = zip_command.format(target_i, source_i)
                print(zip_command_i)
                os.system(zip_command_i)
            else:
                print("{} not exist".format(source_i))


if __name__ == '__main__':
    zip_images_json("hyj")
