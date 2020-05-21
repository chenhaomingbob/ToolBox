#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/27
    Description:
"""

from common import utils_io_folder
import os


def work():
    root_path = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/cropped_image"
    first_paths = utils_io_folder.get_immediate_subfolder_paths(root_path)
    for first_path in first_paths:
        second_paths = utils_io_folder.get_immediate_subfolder_paths(first_path)
        for second_path in second_paths:
            image_paths = utils_io_folder.get_immediate_childfile_paths(second_path)
            if image_paths is None or len(image_paths) == 0:
                os.rmdir(second_path)
            else:
                pa = "/media/jion/D/chenhaoming/experiment/hmr"
                print(pa + second_path[61:])
                # new_path=""
                utils_io_folder.create_folder(pa + second_path[61:])
                # for image_path in image_paths:
                #     dest = image_path + ".jpg"
                #     # print(dest)
                #     os.rename(image_path, dest)


if __name__ == '__main__':
    work()
