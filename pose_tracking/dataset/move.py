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
from tqdm import tqdm


def work():
    cmd = "mv {} {}"
    root_path = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/posetrack_data/images"
    change_path = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/cropped_image/{}/{}"
    folder_paths = utils_io_folder.get_immediate_subfolder_paths(root_path)
    for folder_path in tqdm(folder_paths):
        first_folder_name = utils_io_folder.get_file_name_without_ext_from_path(folder_path)
        # print(first_folder_name)
        paths = utils_io_folder.get_immediate_subfolder_paths(folder_path)
        for path in paths:
            second_folder_name = utils_io_folder.get_file_name_without_ext_from_path(path)
            # print(second_folder_name)
            images_path = utils_io_folder.get_immediate_childfile_paths(path)
            new_path = change_path.format(first_folder_name, second_folder_name)
            utils_io_folder.create_folder(new_path)
            for image_path in images_path:
                image_name = utils_io_folder.get_file_name_without_ext_from_path(image_path)
                if image_name.find("transform") >= 0:
                    cmd_i = cmd.format(image_path, os.path.join(new_path, image_name))
                    os.system(cmd_i)


if __name__ == '__main__':
    work()
