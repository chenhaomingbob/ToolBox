#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/23
    Description: 关于图片的编解码，转换
"""

import base64
import io

import numpy as np
import PIL.ExifTags
import PIL.Image
import PIL.ImageOps

import os
import cv2
import numpy as np
from common import utils_io_folder
from tqdm import tqdm


def img_encode_to_base64(file):
    with open(file, 'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data).decode('utf-8')
        # print(type(base64_data))
        # print(base64_data)
        # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64,
        # base64_str = str(base64_data, 'utf-8')
        # print(base64_str)
        return base64_data


def img_data_to_arr(img_data):
    f = io.BytesIO()
    f.write(img_data)
    img_arr = np.array(PIL.Image.open(f))
    return img_arr


def img_b64_to_arr(img_b64):
    img_data = base64.b64decode(img_b64)
    img_arr = img_data_to_arr(img_data)
    return img_arr


def img_arr_to_b64(img_arr):
    img_pil = PIL.Image.fromarray(img_arr)
    f = io.BytesIO()
    img_pil.save(f, format='PNG')
    img_bin = f.getvalue()
    if hasattr(base64, 'encodebytes'):
        img_b64 = base64.encodebytes(img_bin)
    else:
        img_b64 = base64.encodestring(img_bin)
    return img_b64


def img_data_to_png_data(img_data):
    with io.BytesIO() as f:
        f.write(img_data)
        img = PIL.Image.open(f)

        with io.BytesIO() as f:
            img.save(f, 'PNG')
            f.seek(0)
            return f.read()


def apply_exif_orientation(image):
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None

    if exif is None:
        return image

    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in exif.items()
        if k in PIL.ExifTags.TAGS
    }

    orientation = exif.get('Orientation', None)

    if orientation == 1:
        # do nothing
        return image
    elif orientation == 2:
        # left-to-right mirror
        return PIL.ImageOps.mirror(image)
    elif orientation == 3:
        # rotate 180
        return image.transpose(PIL.Image.ROTATE_180)
    elif orientation == 4:
        # top-to-bottom mirror
        return PIL.ImageOps.flip(image)
    elif orientation == 5:
        # top-to-left mirror
        return PIL.ImageOps.mirror(image.transpose(PIL.Image.ROTATE_270))
    elif orientation == 6:
        # rotate 270
        return image.transpose(PIL.Image.ROTATE_270)
    elif orientation == 7:
        # top-to-right mirror
        return PIL.ImageOps.mirror(image.transpose(PIL.Image.ROTATE_90))
    elif orientation == 8:
        # rotate 90
        return image.transpose(PIL.Image.ROTATE_90)
    else:
        return image


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
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率<每秒中展示多少张图片>
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取宽度
    i = 0
    if outimages_path is not None:
        if not utils_io_folder.folder_exists(outimages_path):
            utils_io_folder.create_folder(outimages_path)
    assert isOpened, "Can't find video"
    for index in tqdm(range(video_length)):
        (flag, data) = cap.read()  # 读取每一张 flag<读取是否成功> frame<内容>
        file_name = "{0:08d}.jpg".format(index + 1)
        if outimages_path is not None:
            file_path = os.path.join(outimages_path, file_name)
        else:
            utils_io_folder.create_folder("output")
            file_path = os.path.join("output", file_name)
        if flag:  # 读取成功的话
            # 写入文件，1 文件名 2 文件内容 3 质量设置
            cv2.imwrite(file_path, data, [cv2.IMWRITE_JPEG_QUALITY, 100])

