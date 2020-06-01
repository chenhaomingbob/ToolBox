#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/05/29
    Description:
"""
from common import utils_io_folder
import shutil
from tqdm import tqdm

train_base_path = "/media/jion/D/chenhaoming/experiment/tubes/384x288/train"

train_subfolder_paths = utils_io_folder.get_immediate_subfolder_paths(train_base_path)

for train_subfolder_path in tqdm(train_subfolder_paths):
    video_paths = utils_io_folder.get_immediate_subfolder_paths(train_subfolder_path)
    for video_path in tqdm(video_paths):
        video_npy_path = utils_io_folder.get_immediate_childfile_paths(video_path)
        shutil.copy(video_npy_path[0], "/media/jion/D/chenhaoming/experiment/tubes/384x288/npy/train/")

val_base_path = "/media/jion/D/chenhaoming/experiment/tubes/384x288/val"

val_subfolder_paths = utils_io_folder.get_immediate_subfolder_paths(val_base_path)

for val_subfolder_path in tqdm(val_subfolder_paths):
    video_paths = utils_io_folder.get_immediate_subfolder_paths(val_subfolder_path)
    for video_path in tqdm(video_paths):
        video_npy_path = utils_io_folder.get_immediate_childfile_paths(video_path)
        shutil.copy(video_npy_path[0], "/media/jion/D/chenhaoming/experiment/tubes/384x288/npy/val/")
