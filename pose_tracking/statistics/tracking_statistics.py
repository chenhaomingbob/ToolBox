#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/19
    Description:
"""
import xlwt, os, sys
from common import utils_json, utils_io_folder

total_name = "total_MOT_metrics"

names = ["right_ankle",
         "right_knee",
         "right_hip",
         "right_shoulder",
         "right_elbow",
         "right_wrist",
         "left_ankle",
         "left_knee",
         "left_hip",
         "left_shoulder",
         "left_elbow",
         "left_wrist",
         "neck",
         "nose",
         "head_top",
         "total",
         ]
types = [
    "num_misses",
    "num_switches",
    "num_false_positives",
    "num_detections",
    "num_matches",
    "num_objects",
    "mota",
    "motp",
    "pre",
    "rec",
]


def start(path):
    file_paths = utils_io_folder.get_immediate_childfile_paths(path)
    mota_paths = []
    for file_path in file_paths:
        file_name = utils_io_folder.get_file_name_without_ext_from_path(file_path)
        if file_name.find("MOT") > 0:
            mota_paths.append(file_path)

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("sheet 1")
    sheet.write(0, 0, " ")
    i = 1
    for type in types:
        for name in names:
            sheet.write(i, 0, "{}-{}".format(type, name))
            i += 1
        sheet.write(i, 0, "")
        i += 1
    j = 1
    for file_path in mota_paths:
        file_name = utils_io_folder.get_file_name_without_ext_from_path(file_path)
        if file_name != total_name:
            index = file_name.find("_mpii")
            video_number = file_name[0:int(index)]
        else:
            video_number = "total"
        sheet.write(0, j, video_number)
        json_data = utils_json.read_json_from_file(file_path)
        i = 1
        for type in types:
            type_json_data = json_data[type]
            for index, _ in enumerate(names):
                sheet.write(i, j, type_json_data[index])
                i += 1
            sheet.write(i, j, "")
            i += 1
        j += 1

    interval_index = path.rindex("/")
    source_index = path.rindex("/", 0, interval_index)
    wbk.save("{}_{}.xls".format(path[source_index + 1:interval_index], path[interval_index + 1:]))


if __name__ == '__main__':
    path = "C:/Users/chenh/Desktop/sta/lightrack/interval=3"
    start(path)
