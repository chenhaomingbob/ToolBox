#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/07
    Description:
"""
import sys

# import utils_image, utils_io_folder
print(sys.path)

if __name__ == '__main__':
    a = "/media/jion/D/chenhaoming/DataSet/DouYin/images/滑板/{0:06d}.zip"
    str1 = ""
    for i in range(1, 11):
        str1 = str1 + " " + a.format(i)
    print(str1)
    # folder = "F:/DataSet/douyin/images/dance"
    # subfolders = utils_io_folder.get_immediate_subfolder_paths(folder)
    # for subfolder in subfolders:
    #     video_name = utils_io_folder.get_file_name_without_ext_from_path(subfolder)
    #     image_paths = utils_io_folder.get_immediate_childfile_paths(subfolder,ext="jpg")
    #     output_path = "F:/DataSet/douyin/videos/dance/{}.mp4".format(video_name)
    #     # print(output_path)
    #     utils_image.make_video_from_images(image_paths, output_path)
    # utils_image.make_video_from_images()
