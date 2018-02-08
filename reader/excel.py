#!/usr/bin/env python
#!coding:utf-8
import xlrd
import reader.tree as tree
import uuid

def read_excel(excel_file):
    """ 读取文档
    :param excel_file: 文件名
    :return:  创建好一棵树
    """
    header = []
    body = []
    trees = tree.tree()

    excel = xlrd.open_workbook(excel_file)
    sheets = excel.sheet_names()
    for sheet in sheets:
        sheet = excel.sheet_by_name(sheet)
        for row_value in range(sheet.nrows):
            values = sheet.row_values(row_value)
            if row_value == 0:
                continue
            if row_value == 1:
                for value in values:
                    header.append(value.strip())
                continue
            values[0] = str(uuid.uuid1())
            body.append(values)
    return crate_tree(trees,header,body)


def crate_tree(trees,header,body):
    """创建树
    :return: 创建好一棵树
    """
    # 在每个树头最后都加上一个UUID
    header[0] = "UUID"
    loop = len(header)
    for b in body:
        for i in range(loop):
            trees[b[i]][header[0]] = b[0]
            trees[b[0]][header[i]] = b[i]
    return trees
