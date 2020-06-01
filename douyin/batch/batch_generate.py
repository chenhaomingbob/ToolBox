#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/01
    Description: 运行openpose
"""

import os, sys

sys.path.append(os.path.abspath(r"../../"))
import common.utils_io_folder
from douyin.batch.config import video_types


def start(type, hand=False, skip=False):
    assert type in video_types
    yin = "/media/jion/D/chenhaoming/DataSet/DouYin"
    image_dir = "{}/images/{}".format(yin, type)
    # write_json_base = "/media/D/DataSet/DouYin/images/{}/{0:06d}/openpose"
    write_json_base = "{}/machine_openpose/{}".format(yin, type)
    if common.utils_io_folder.folder_exists(write_json_base) and skip:
        return
    openpose = "/media/jion/D/chenhaoming/Code/openpose"
    cmd = "%s/build/examples/openpose/openpose.bin --image_dir {} --write_json {} " % openpose
    if hand:
        cmd = cmd + " --hand"
    des = "%s" % openpose
    os.chdir(des)
    subfolder_paths = common.utils_io_folder.get_immediate_subfolder_paths(image_dir)
    for subfolder_path in subfolder_paths:
        video_name = common.utils_io_folder.get_file_name_without_ext_from_path(subfolder_path)
        write_json = os.path.join(write_json_base, video_name)
        if not os.path.exists(write_json):
            common.utils_io_folder.create_folder(write_json)

        os.system(cmd.format(subfolder_path, write_json))




if __name__ == '__main__':

    start("other", hand=True, skip=False)
