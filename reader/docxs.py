#!/usr/bin/env python
#!coding:utf-8
import docx
import uuid
import reader.tree as tree
import random
import string

# 创建一个颗树
trees = tree.tree()


def salt():
    """生成随机盐"""
    return ''.join(random.sample(string.ascii_letters, 4))


def reader_doc(doc_name):
    """读取文档
    :param doc_name:  读取文档名
    :return:  创建好一棵树
    """
    doc = docx.Document(doc_name)
    for s, t in enumerate(doc.tables):
        head = []
        body = []
        max_row = 1 if len(t.rows[0].cells) < len(t.rows[1].cells) else 0
        for i, r in enumerate(t.rows[max_row:]):
            for c in r.cells:
                if i == 0:
                    head.append(c.text)
                    continue
                else:
                    body.append(c.text)
            if i != 0:
                body.append(str(uuid.uuid1()))
        crate_tree(head, body)
    return trees


def crate_tree(head, body):
    """创建一棵树
    :param head: 树头
    :param body:  节点
    """
    head.append("uuid")
    global trees
    loop = len(head)
    last = loop - 1
    _all = len(body)
    for i in range(int(_all / loop)):
        for j in range(loop - 1):
            _cell = body[i * loop + j]
            _uuid = body[last + i * loop]
            node = trees[_cell]
            if len(node) != 0:
                node[head[last] + salt()] = _uuid
            else:
                node[head[last]] = _uuid
            trees[_uuid][head[j]] = _cell
