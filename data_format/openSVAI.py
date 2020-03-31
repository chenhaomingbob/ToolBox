#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/23
    Description:
"""
import json
import os


class OpenSVAI_JSON(object):

    def __init__(self, filename=None):
        self.frames = []
        self.video_name = ""
        self.path = ""
        if filename != None:
            self.load_json(filename)

    def load_json(self, filename):
        # assert type(json_data)==
        file = open(filename, encoding='utf-8')
        self.frames = json.load(file)
        self.video_name = os.path.basename(filename)
        self.path = os.path.dirname(filename)

    def __len__(self):
        return len(self.frames)


if __name__ == '__main__':
    # name = "/media/jion/D/chenhaoming/DataSet/PoseTrack2017/posetrack_data/images/bonn_5sec/000342_mpii"
    # print(os.path.basename(name))
    # print(os.path.dirname(name))
    a = [0]*10
    a[10] = 1

