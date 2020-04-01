#!/usr/bin/python
# -*- coding:utf8 -*-
"""
    Author: Haoming Chen
    E-mail: chenhaomingbob@163.com
    Time: 2020/04/01
    Description:
"""

import os

if __name__ == '__main__':
    image_dir = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}"
    write_json = "/media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/openpose"
    cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir {} --write_json {} --hand"
    des = "/media/jion/D/chenhaoming/Code/openpose"
    os.chdir(des)
    for i in range(1, 36):
        image_dir.format(i)
        write_json.format(i)
        cmd.format(image_dir, write_json)
        os.system(cmd.format(i, i))
