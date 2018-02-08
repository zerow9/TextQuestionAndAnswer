#!/usr/bin/env python
#!coding:utf-8
from article_sturction_judge import article_sturction_judge_main
from semiStructured import semi_structured_main
from readDocx import sentencesMain

if __name__ == '__main__':
    # dictMerged = dict(dict(article_sturction_judge_main("nineteenReportDocuments.docx"),
    #                         **sentencesMain("nineteenReportDocuments.docx")),
    #                    **semi_structured_main("text"))
    # print(len(dictMerged.keys()))
    # print(len(article_sturction_judge_main("nineteenReportDocuments.docx").keys()))
    # print(len(sentencesMain("nineteenReportDocuments.docx").keys()))
    print(len(semi_structured_main("text").keys()))

