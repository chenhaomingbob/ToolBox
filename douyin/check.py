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
    # cmd = "/media/jion/D/chenhaoming/Code/openpose/build/examples/openpose/openpose.bin --image_dir /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d} --write_json /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/openpose --hand"
    des = "/media/jion/D/chenhaoming/Downloads"
    # cmd = "mv /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}/openpose /media/jion/D/chenhaoming/DataSet/DouYin/images/openpose/dance/{0:06d}"
    os.chdir(des)
    cmd = "./BaiduPCS-Go"
    os.system(cmd)
    for i in range(10, 13):
        cmd = "upload /media/jion/D/chenhaoming/DataSet/DouYin/images/dance/{0:06d}.zip DouYin".format(i)
        os.system(cmd)
# for i in range(1, 36):
#     os.system(cmd.format(i, i))
