#!/usr/bin/env python
# !coding:utf-8

import json

from dataPreprocessing.article_sturction_judge import article_sturction_judge_main
from dataPreprocessing.readDocx import sentencesMain
from dataPreprocessing.semiStructured import semi_structured_main
from databaseInterface.database import *

def main(own_user,article_name,article_path,from_field):
    '''
    :param own_user:上传用户
    :param article_name:文件名
    :param article_path:文件保存路径
    :param from_field:文章所属领域/类型
    :return:问题的json数据返回；key:question，value:answer
    :article_sturction_judge_main：段间问答
    :sentencesMain：句内问答
    :semi_structured_main：半结构化数据问答
    '''
    operating = Database("192.168.160.36", "user_zwb", "123456", "grammer", 3306)
    articleName = operating.selectDataArticleName()
    if article_name not in articleName:
        operating.insertDataArticle(own_user,article_name,article_path,from_field)
    dictMerged = {}
    if article_path.endswith('docx'):
        readDocx = sentencesMain(article_path)
        article_sturction_judge_mainText = article_sturction_judge_main(article_path)
        dictMerged = dict(dict(dictMerged,**readDocx),**article_sturction_judge_mainText)
    if article_path.endswith('xls'):
        semi_structured_mainText = semi_structured_main(article_path)
        dictMerged = dict(dictMerged,**semi_structured_mainText)
    print(len(dictMerged.keys()))
    # dictMerged = dict(dict(article_sturction_judge_main(noStructureDataPath),
    #                        **sentencesMain(noStructureDataPath)),
    #                   **semi_structured_main(semiStructuredDataPathFolder))
    return json.dumps(dictMerged, ensure_ascii=False)


if __name__ == '__main__':
    print(main(23,'nineteenReportDocuments.docx','nineteenReportDocuments.docx','政治'))
    # dictMerged = dict(dict(sentencesMain("nineteenReportDocuments.docx"),
    #                        **article_sturction_judge_main("nineteenReportDocuments.docx")),
    #                   **semi_structured_main("text"))
    # print(len(dictMerged.keys()))
    # print(json.loads(main("nineteenReportDocuments.docx", "text")))
    # print(len(dictMerged.keys()))
    # print(len(article_sturction_judge_main("nineteenReportDocuments.docx").keys()))
    # print(len(sentencesMain("nineteenReportDocuments.docx").keys()))
    # print(len(semi_structured_main("text").keys()))
