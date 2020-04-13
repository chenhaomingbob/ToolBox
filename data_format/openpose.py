#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/01
    Description:
"""

import json
import os

keypoints_order = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder ankle", "LElbow",
                   "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye",
                   "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"
                   ]

import numpy

thresold = 0.2


class OpenPose_JSON(object):

    def __init__(self, filename=None):
        self.version = ""
        self.video_name = ""
        self.path = ""
        self.people = []
        if filename != None:
            self.load_json(filename)

    def load_json(self, filename):
        # assert type(json_data)==
        file = open(filename, encoding='utf-8')
        frame_data = json.load(file)
        self.video_name = os.path.basename(filename)
        self.path = os.path.dirname(filename)
        raw_people = frame_data["people"]
        next_id = 0
        for raw_person in raw_people:
            person = dict()
            person_id = raw_person["person_id"][0]
            if person_id == -1:
                person_id = next_id
                next_id += 1
            person["person_id"] = person_id
            person["pose_keypoints_2d"] = numpy.array(raw_person["pose_keypoints_2d"]).reshape(-1, 3)
            person["hand_left_keypoints_2d"] = numpy.array(raw_person["hand_left_keypoints_2d"]).reshape(-1, 3)
            person["hand_right_keypoints_2d"] = numpy.array(raw_person["hand_right_keypoints_2d"]).reshape(-1, 3)
            for i in range(len(person["pose_keypoints_2d"])):
                if person["pose_keypoints_2d"][i][2] < thresold:
                    person["pose_keypoints_2d"][i][0], person["pose_keypoints_2d"][i][1] = 0, 0
            for i in range(len(person["hand_left_keypoints_2d"])):
                if person["hand_left_keypoints_2d"][i][2] < thresold:
                    person["hand_left_keypoints_2d"][i][0], person["hand_left_keypoints_2d"][i][1] = 0, 0
            for i in range(len(person["hand_right_keypoints_2d"])):
                if person["hand_right_keypoints_2d"][i][2] < thresold:
                    person["hand_right_keypoints_2d"][i][0], person["hand_right_keypoints_2d"][i][1] = 0, 0
            self.people.append(person)

    def __len__(self):
        return len(self.people)
