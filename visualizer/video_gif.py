#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/24
    Description:
"""

import os
import cv2
import numpy as np
import utils_io_folder


def make_video_from_images(img_paths, outvid_path, fps=25, size=None,
                           is_color=True, format="XVID"):
    """
    Create a video from a list of images.

    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for ct, img_path in enumerate(img_paths):
        if not os.path.exists(img_path):
            raise FileNotFoundError(img_path)
        img = imread(img_path)
        if img is None:
            print(img_path)
            continue
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid_path, fourcc, float(fps), size, is_color)

        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    if vid is not None:
        vid.release()
    return vid


def make_gif_from_images(img_paths, outgif_path):
    import imageio
    resize_ratio = 4
    skip_ratio = 2

    with imageio.get_writer(outgif_path, mode='I') as writer:
        for img_id, img_path in enumerate(img_paths):
            image = imageio.imread(img_path)
            image_resize = image[::resize_ratio, ::resize_ratio, :]
            # Do sth to make gif file smaller
            # 1) change resolution
            # 2) change framerate
            if img_id % skip_ratio == 0:
                writer.append_data(image_resize)
    print("Gif made!")
    return


def make_images_from_video(video_path, outimages_path=None):
    cap = cv2.VideoCapture(video_path)
    isOpened = cap.isOpened()
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率<每秒中展示多少张图片>
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取宽度
    i = 0
    while (isOpened):  # 当视频被打开了
        i = i + 1  # i++
        (flag, frame) = cap.read()  # 读取每一张 flag<读取是否成功> frame<内容>
        file_name = "{0:08d}.jpg".format(i)
        if outimages_path is not None:
            utils_io_folder.create_folder(outimages_path)
            file_path = os.path.join(outimages_path, file_name)
        else:
            utils_io_folder.create_folder("output")
            file_path = os.path.join("output", file_name)
        if flag:  # 读取成功的话
            # 写入文件，1 文件名 2 文件内容 3 质量设置
            cv2.imwrite(file_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])


if __name__ == '__main__':
    # make_images_from_video(video_path="C:/Users/chenh/Desktop/compare/openpose_output/16662.avi",
    #                        outimages_path="C:/Users/chenh/Desktop/compare/openpose_output/decompose_images")
    img_paths = utils_io_folder.get_immediate_childfile_paths(
        "C:/Users/chenh/Desktop/compare/openpose_output/decompose_images/")

    make_video_from_images(img_paths=img_paths,
                           outvid_path="C:/Users/chenh/Desktop/compare/openpose_output/test.avi")
    # img_path = ""
    # outvid_path = ""
    # make_video_from_images(img_paths=, outvid_path=)
