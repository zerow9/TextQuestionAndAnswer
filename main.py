#!/usr/bin/env python
#!coding:utf-8
from article_sturction_judge import article_sturction_judge_main
from semiStructured import semi_structured_main
from readDocx import sentencesMain
import json

def main(noStructureDataPath,semiStructuredDataPathFolder):
    '''
    :param noStructureDataPath: 只能是无结构化的数据文件
    :param semiStructuredDataPathFolder:可以是半结构化的数据文件，也可以是半结构化的数据文件夹
    :return:问题的json数据返回；key:question，value:answer
    :article_sturction_judge_main：段间问答
    :sentencesMain：句内问答
    :semi_structured_main：半结构化数据问答
    '''
    dictMerged = dict(dict(article_sturction_judge_main(noStructureDataPath),
                           **sentencesMain(noStructureDataPath)),
                      **semi_structured_main(semiStructuredDataPathFolder))
    return json.dumps(dictMerged,ensure_ascii=False)

if __name__ == '__main__':
    dictMerged = dict(dict(article_sturction_judge_main("nineteenReportDocuments.docx"),
                            **sentencesMain("nineteenReportDocuments.docx")),
                       **semi_structured_main("text"))
    print(json.loads(main("nineteenReportDocuments.docx","text")))
    # print(len(dictMerged.keys()))
    # print(len(article_sturction_judge_main("nineteenReportDocuments.docx").keys()))
    # print(len(sentencesMain("nineteenReportDocuments.docx").keys()))
    # print(len(semi_structured_main("text").keys()))
