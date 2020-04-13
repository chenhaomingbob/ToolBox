#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/09
    Description:
"""
import os, sys
from tqdm import tqdm

sys.path.append(os.path.abspath(r"../../"))
import common.utils_io_folder


def mv1():
    cmd = "mv {} {}"
    # source_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/machine_openpose/KongFu/{0:06d}/*.json"
    # des_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/KongFu/{0:06d}"
    source_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/KongFu/{0:06d}/*.json"
    des_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/machine_openpose/KongFu/{0:06d}"

    for i in tqdm(range(1, 41)):
        source_dir_i = source_dir.format(i)
        des_dir_i = des_dir.format(i)
        common.utils_io_folder.create_folder(des_dir_i)
        print(cmd.format(source_dir_i, des_dir_i))
        os.system(cmd.format(source_dir_i, des_dir_i))


def mv2():
    cmd = "mv {} {}"
    source_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/hyj"
    subfolder_paths = common.utils_io_folder.get_immediate_subfolder_paths(source_dir)
    for subfolder in subfolder_paths:
        file_path = common.utils_io_folder.get_immediate_childfile_paths(subfolder)
        index = 1
        for file_path in file_path:
            cmd_i = cmd.format(file_path, os.path.join(subfolder, "{0:06d}.jpg".format(index)))
            index += 1
            os.system(cmd_i)

    # for i in tqdm(range(1, 41)):
    #     source_dir_i = source_dir.format(i)
    #     des_dir_i = des_dir.format(i)
    #     common.utils_io_folder.create_folder(des_dir_i)
    #     print(cmd.format(source_dir_i, des_dir_i))
    #     os.system(cmd.format(source_dir_i, des_dir_i))


if __name__ == '__main__':
    mv2()
