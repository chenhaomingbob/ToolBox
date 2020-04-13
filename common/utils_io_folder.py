#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/24
    Description:
"""

import os
from common.utils_natural_sort import natural_sort


def get_immediate_subfolder_paths(folder_path):
    subfolder_names = get_immediate_subfolder_names(folder_path)
    subfolder_paths = [os.path.join(folder_path, subfolder_name) for subfolder_name in subfolder_names]
    return subfolder_paths


def get_immediate_subfolder_names(folder_path):
    subfolder_names = [folder_name for folder_name in os.listdir(folder_path)
                       if os.path.isdir(os.path.join(folder_path, folder_name))]
    natural_sort(subfolder_names)
    return subfolder_names


def get_immediate_childfile_paths(folder_path, ext=None, exclude=None):
    files_names = get_immediate_childfile_names(folder_path, ext, exclude)
    files_full_paths = [os.path.join(folder_path, file_name) for file_name in files_names]
    return files_full_paths




def get_immediate_childfile_names(folder_path, ext=None, exclude=None):
    files_names = [file_name for file_name in next(os.walk(folder_path))[2]]
    if ext is not None:
        files_names = [file_name for file_name in files_names
                       if file_name.endswith(ext)]
    if exclude is not None:
        files_names = [file_name for file_name in files_names
                       if not file_name.endswith(exclude)]
    natural_sort(files_names)
    return files_names


def get_file_name_from_path(file_path):
    path, file_name = os.path.split(file_path)
    return file_name


def get_file_name_without_ext_from_path(file_path):
    """

    :param file_path:
    :return:  without extension
    """
    file_name = get_file_name_from_path(file_path)
    pure_name = get_file_name_without_ext_from_name(file_name)
    return pure_name


def get_file_name_without_ext_from_name(file_name):
    pure_name, ext = os.path.splitext(file_name)
    return pure_name


def replace_file_ext(file_name, ext):
    pure_name = get_file_name_without_ext_from_name(file_name)
    return "{}.{}".format(pure_name, ext)


def get_parent_folder_from_path(folder_path):
    parent_folder_path = os.path.abspath(os.path.join(folder_path, os.pardir))
    return parent_folder_path


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def folder_exists(folder_path):
    return os.path.exists(folder_path)


def rename_filename_concation_openSVAI(filename):
    new_filename = filename.replace("_OpenSVAI", "")
    os.rename(filename, new_filename)
    return new_filename


if __name__ == '__main__':

    path = "/media/jion/D/chenhaoming/experiment/contrast/exp_lighttrack_official_CPN101_posetrack18_val_gt_interval_3/jsons"
    for filepath in get_immediate_childfile_paths(path):
        rename_filename_concation_openSVAI(filepath)
