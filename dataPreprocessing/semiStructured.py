#!/usr/bin/env python
# !coding:utf-8
from databaseInterface.database import *
import reader.docxs as doc
import reader.excel as excel
import reader.tree as f
import reader.mysql as mysql
import reader.tree as tree
import os


def semi_structured_main(path):
    operating = Database("192.168.160.36", "user_zwb", "123456", "grammer", 3306)
    allQuestion = operating.selectDataQuestionAnswerQuestion("=''")
    files = []
    questionAnswer = {}
    if os.path.isfile(path):
        files.append(path)
    else:
        files = f.dirs(path, files)
    for file in files:
        file_name = file.split("\\")[-1]
        trees = None
        if file.endswith(".docx"):
            trees = doc.reader_doc(file)
        if file.endswith(".xls"):
            trees = excel.read_excel(file)
        question = mysql.ergodic_tree(trees, file_name)
        articleId = operating.selectDataArticleByArticleName(file_name)
        for key in question:
            if key not in allQuestion:
                operating.insertDataQuestionAnswer(articleId,'','',key,question[key])
        questionAnswer = dict(questionAnswer, **(question))
    return questionAnswer


if __name__ == '__main__':
    print(semi_structured_main("../text"))
