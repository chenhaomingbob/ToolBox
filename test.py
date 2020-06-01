#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/05/27
    Description:
"""
import cv2

video_path = "E:/Code/vehicle_detector/segment-1.avi"
video = cv2.VideoCapture(video_path)
if not video.isOpened():
    print("meikai")
else:
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    new_h = int(height / 2 / 4 * 4)
    new_w = int(width / 2 / 4 * 4)
    count = 0
    while (True):
        ret, frame = video.read()  # 捕获一帧图像
        count += 1000000
        if ret:
            frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            print((int(new_w / 2 - 50), int(new_h / 2 - 10)))
            imgzi = cv2.putText(frame, str(count), (int(new_w / 2 - 50), int(new_h / 2 - 10)),
                                cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3,
                                (0, 0, 255), 3)
            cv2.imshow('frame', imgzi)
            cv2.waitKey(20000)
