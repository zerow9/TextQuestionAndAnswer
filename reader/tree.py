from collections import defaultdict
import os


def tree():
    """创建树"""
    return defaultdict(tree)


def dirs(_dir):
    """ 遍历文件夹
    :param _dir:  文件夹名字
    """
    file = []
    for (root, dirs_, files) in os.walk(_dir):
        for filename in files:
            name = os.path.join(root, filename)
            file.append(name)
        for d in dirs_:
            os.path.join(root, d)
    return file


def ask_answer(trees, _ask):
    """ 测试问答对，问答对问题和标签用逗号隔开(ask,label)
    :param trees:  树
    :param _ask:  问答对
    """
    sentence = _ask.split(',')
    keys = trees[sentence[0]]
    for v in keys:
        key = keys[v]
        value = trees[key][sentence[1]]
        if len(value) != 0:
            print(value)
