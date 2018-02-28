#!/usr/bin/env python
# !coding:utf-8
from databaseInterface.database import *
from itertools import chain
from docx import Document
import pandas as pd
import numpy as np
import copy
import docx
import math
import json
import re


def make_main_para(article, paragraph_head_order):
    # paragraph_head_order="[*]|{*}|\(*\)|（*）|[一二三四五六七八九十]{1,3}[、.]|[0-9]{1,3}[、.]|【*】"
    para_1 = '[*]'
    para_2 = '{*}'
    para_3 = '\(*\)'
    para_4 = '（*）'
    para_5 = '[一二三四五六七八九十]{1,3}[、.]'
    para_6 = '[0-9]{1,3}[、.]'
    para_7 = '【*】'

    # find paragraph order
    head_order_list = []
    head_order_1 = []
    head_order_2 = []
    head_order_3 = []
    head_order_4 = []
    head_order_5 = []
    head_order_6 = []
    head_order_7 = []

    for para in article:
        head_order = re.findall(paragraph_head_order, para[0:8])
        head_1 = re.findall(para_1, para[0:8])
        head_2 = re.findall(para_2, para[0:8])
        head_3 = re.findall(para_3, para[0:8])
        head_4 = re.findall(para_4, para[0:8])
        head_5 = re.findall(para_5, para[0:8])
        head_6 = re.findall(para_6, para[0:8])
        head_7 = re.findall(para_7, para[0:8])

        if (head_order != []):
            head_order_list.append(article.index(para))
        if (head_1 != []):
            head_order_1.append(article.index(para))
        if (head_2 != []):
            head_order_2.append(article.index(para))
        if (head_3 != []):
            head_order_3.append(article.index(para))
        if (head_4 != []):
            head_order_4.append(article.index(para))
        if (head_5 != []):
            head_order_5.append(article.index(para))
        if (head_6 != []):
            head_order_6.append(article.index(para))
        if (head_7 != []):
            head_order_7.append(article.index(para))

        head_final = {1: head_order_1, 2: head_order_2, 3: head_order_3, 4: head_order_4, 5: head_order_5,
                      6: head_order_6, 7: head_order_7}
        para_importance = {}
        para_importance[1] = np.std(head_order_1)
        para_importance[2] = np.std(head_order_2)
        para_importance[3] = np.std(head_order_3)
        para_importance[4] = np.std(head_order_4)
        para_importance[5] = np.std(head_order_5)
        para_importance[6] = np.std(head_order_6)
        para_importance[7] = np.std(head_order_7)

    for i in range(1, 8):
        if (math.isnan(para_importance[i])):
            del para_importance[i]

    importance_order = list(sorted(zip(para_importance.values(), para_importance.keys()), reverse=True))
    para_order_final = {}
    if (importance_order != []):
        for i in range(0, len(importance_order)):
            num = importance_order[i][1]
            para_order_final[i] = head_final[num]
        return (para_order_final)


def para_mid_QA(article, important_struction, paragraph_head_order,path):
    # paragraph_head_order="[*]|{*}|\(*\)|（*）|[一二三四五六七八九十]{1,3}[、.]|[0-9]{1,3}[、.]|【*】"
    operating = Database("192.168.160.36", "user_zwb", "123456", "grammer", 3306)
    keys_list = []
    values_list = []

    for keys, values in important_struction.items():
        values_list.append(values)
        keys_list.append(list(np.repeat(keys, len(values))))

    values_list = list(chain(*values_list))
    keys_list = list(chain(*keys_list))

    para_order_construction = {"values": values_list, "keys": keys_list}
    para_order_construction = pd.DataFrame(para_order_construction)
    para_order_construction = para_order_construction.sort_values(by="values", axis=0)
    para_order_construction = para_order_construction.reset_index(drop=True)
    QA_list = {}
    for layer in range(len(set(para_order_construction["keys"])) - 2, -1, -1):
        for row_num in range(0, len(para_order_construction) - 1):
            answer_list = []
            if (para_order_construction["keys"][row_num]) == layer:
                for row_num_small in range(row_num + 1, len(para_order_construction) - 1):
                    if (para_order_construction["keys"][row_num_small] > layer):
                        answer_list.append(para_order_construction["values"][row_num_small])
                        continue
                    else:
                        break
            if (answer_list != []):
                QA_list[para_order_construction["values"][row_num]] = answer_list

    QA_list_final = {}
    arctileId = operating.selectDataArticleByArticleName(path.replace('\\','/').split('/')[-1])
    for key, value in QA_list.items():
        key = article[key]
        key = re.sub(paragraph_head_order, "", key, 1)
        paragraphId = operating.selectDataParagraph(arctileId,key)
        key += "包括哪些方面?"
        value_final = []
        for value_small in value:
            value_small = article[value_small]
            value_small = value_small.split("。")[0]
            tmp = value_small.replace("　", '')
            value_final.append(tmp)
            praID = operating.selectDataParagraph(arctileId,tmp)
            if len(praID)>0:
                paragraphId.extend(praID)
        QA_list_final[key.replace("　", '')] = value_final
        paragraph = operating.selectDataQuestionAnswerQuestion("=''")
        if key.replace("　", '') in paragraph:
            continue
        data = {'article_sentences_number': '\"' + str(important_struction) + '\"'}
        articleId = operating.selectDataArticleByArticleName(path.replace('\\', '/').split('/')[-1])
        operating.updateDataArticle(articleId, **data)
        operating.insertDataQuestionAnswer(arctileId,paragraphId,'',key.replace("　", ''),value_final)
    return QA_list_final


def article_sturction_judge_main(path):
    # path = "nineteenReportDocuments.docx"
    document = Document(path)
    article = []
    for paragraph in document.paragraphs:
        article.append(paragraph.text)
    paragraph_head_order = "[*]|{*}|\(*\)|（*）|[一二三四五六七八九十]{1,3}[、.]|[0-9]{1,3}[、.]|【*】"
    important_struction = make_main_para(article, paragraph_head_order)  # 中间结果
    questionAnswer = para_mid_QA(article, important_struction, paragraph_head_order,path)
    return questionAnswer


if __name__ == '__main__':
    print(article_sturction_judge_main("../nineteenReportDocuments.docx"))
