#!/usr/bin/env python
#!coding:utf-8
import reader.docxs as doc
import reader.excel as excel
import reader.tree as f
import reader.mysql as mysql
import reader.tree as tree

def semi_structured_main(fileDirs):
    files = f.dirs(fileDirs)
    questionAnswer = {}
    for file in files:
        file_name = file.split("\\")[-1]
        trees = None
        if file.endswith(".docx"):
            trees = doc.reader_doc(file)
        if file.endswith(".xls"):
            trees = excel.read_excel(file)
        questionAnswer = dict(questionAnswer,**(mysql.ergodic_tree(trees, file_name)))
    return questionAnswer

if __name__ == '__main__':
    semi_structured_main("text")

