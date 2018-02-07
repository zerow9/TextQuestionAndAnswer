#!/usr/bin/env python
#!coding:utf-8
from article_sturction_judge import article_sturction_judge_main
from semiStructured import semi_structured_main
from readDocx import sentencesMain

if __name__ == '__main__':
    dictMerged2 = dict(article_sturction_judge_main("nineteenReportDocuments.docx"), **sentencesMain("nineteenReportDocuments.docx"))
    # print(article_sturction_judge_main("nineteenReportDocuments.docx"))
    # print(sentencesMain("nineteenReportDocuments.docx"))
    # print(semi_structured_main("text"))
    print(dict(dictMerged2,**semi_structured_main("text")))

