#!/usr/bin/env python
# !coding:utf-8
from collections import defaultdict
import os


def tree():
    """创建树"""
    return defaultdict(tree)


def dirs(_dir, fileList):
    """ 遍历文件夹
    :param _dir:  文件夹名字
    """
    for (root, dirs_, files) in os.walk(_dir):
        for filename in files:
            name = os.path.join(root, filename)
            fileList.append(name)
        for d in dirs_:
            os.path.join(root, d)
    return fileList
