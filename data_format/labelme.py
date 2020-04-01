#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/03/23
    Description: labelme json format
"""

import os
import PIL.Image
import io
from common import utils_image
import logger
import json
import numpy as np


class Labelme_JSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(Labelme_JSON, self).default(obj)

    def __init__(self):
        self.version = "4.2.9"
        self.flags = {}
        self.shapes = []
        self.imagePath = ""
        self.imageData = ""
        self.imageHeight = 0
        self.imageWidth = 0

    @staticmethod
    def load_image_file(filename):
        try:
            image_pil = PIL.Image.open(filename)
        except IOError:
            logger.error('Failed opening image file: {}'.format(filename))
            return

        # apply orientation to image according to exif
        image_pil = utils_image.apply_exif_orientation(image_pil)

        with io.BytesIO() as f:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg', '.jpeg']:
                format = 'JPEG'
            else:
                format = 'PNG'
            image_pil.save(f, format=format)
            f.seek(0)
            return f.read()

    def to_dict(self):
        # key = ["version", "flag", "shapes", "imagePath", "imageData", "imageHeight", "imageWidth"]
        data = dict(
            version=self.version,
            flags=self.flags,
            shapes=self.shapes,
            imagePath=self.imagePath,
            imageData=self.imageData,
            imageHeight=self.imageHeight,
            imageWidth=self.imageWidth,
        )

        return data
