#!/usr/bin/env python
#!coding:utf-8
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import pymysql

def wide_table_maker():
    connection = pymysql.connect(host='192.168.160.36', port=3306, user='user_zwb', password='123456', db='grammer',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    baidu_result=[]
    feedback_result=[]
    sql = "SELECT baiduResult_id,sentence,baiduResult FROM baiduResult"
    sql1="SELECT * FROM questionAnswer"
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
    for data in result:
        baidu_result.append(data)
    baidu_result=pd.DataFrame(baidu_result)
    cursor.execute(sql1)
    connection.commit()
    result = cursor.fetchall()
    connection.close()
    for data in result:
        feedback_result.append(data)
    feedback_result=pd.DataFrame(feedback_result)
    feedback_result=feedback_result.loc[feedback_result["from_produce"]!='',:]
    baidu_result.columns=['baiduResult','from_produce','sentence']
    data_all=pd.merge(baidu_result,feedback_result,how = 'left',on='from_produce')
    #问题字符长度
    data_all["question_len"]=0
    for i in range(0,len(data_all)):
        data_all.loc[i,"question_len"]=len(data_all.loc[i,"question"])
    #原文本字符长度
    data_all["sentence_len"]=0
    for i in range(0,len(data_all)):
        data_all.loc[i,"sentence_len"]=len(data_all.loc[i,"sentence"])
    
    #deprel结果遍历二元分布
    deprel_all=[]
    postag_all=[]
    for i in range(0,len(data_all)):
        baiduResult=data_all.loc[i,"baiduResult"]
        baiduResult=eval(baiduResult)
        for j in range(0,len(baiduResult['items'])):
            deprel_all.append(baiduResult['items'][j]['deprel'])
            postag_all.append(baiduResult['items'][j]['postag'])
    
    deprel_all=set(deprel_all)
    postag_all=set(postag_all)
    
    #初始化
    for i in deprel_all:
        data_all[i]=0
    for i in postag_all:
        data_all[i]=0
    
    for i in range(0,len(data_all)):
        baiduResult=data_all.loc[i,"baiduResult"]
        baiduResult=eval(baiduResult)
        for j in range(0,len(baiduResult['items'])):
            deprel=baiduResult['items'][j]['deprel']
            postag=baiduResult['items'][j]['postag']
            data_all.loc[i,deprel]=1
            data_all.loc[i,postag]=1
    
    #答案个数
    data_all["answer_num"]=0
    for i in range(0,len(data_all)):
        data_all.loc[i,"answer_num"]=len(data_all.loc[i,"answer"])
    return(data_all)

def question_score(data_all):
    data_all=data_all.drop(["baiduResult","sentence","answer","commit_time","from_paragraph","own_article","produce_time","question","from_produce"],axis=1)
    
    train=pd.DataFrame()
    test=pd.DataFrame()
    
    for i in range(0,len(data_all)):
        if(data_all.loc[i,"yes_or_no"] is None):
            test.append(data_all.loc[i,:])
        else:
            train.append(data_all.loc[i,:])
    
    no_judge=data_all["yes_or_no"]!=1
    no_judge2=data_all["yes_or_no"]!=0
    
    train=data_all.loc[no_judge & no_judge2 != True,:]
    test=data_all.loc[no_judge & no_judge2,:]
    
    
    
    # '''
    import random
    train=data_all.loc[0:1000,:]
    test=data_all.loc[1001:1383,:]
    
    train=train.reset_index(drop=True)
    test=test.reset_index(drop=True)
    
    for i in range(0,len(train)):
        train.loc[i,"yes_or_no"]=random.randint(0,1)
        train.loc[i,"modify"]=random.randint(0,1)
        train.loc[i,"form_user"]=random.randint(0,10)
    
    for i in range(0,len(test)):
        test.loc[i,"form_user"]=random.randint(0,10)
    
    # '''
    #前提是user_id必须得有值
    
    
    train_data=train.drop(["yes_or_no","modify","credibility","questionAnswer_id"],axis=1)
    train_target1=np.asarray(train["yes_or_no"],dtype=np.float64)
    train_target2=train["modify"]
    test_data=test.drop(["yes_or_no","modify","credibility","questionAnswer_id"],axis=1)
    test_target=test[["questionAnswer_id","credibility"]]
    
    
    rf = RandomForestClassifier(criterion='gini', 
                                 n_estimators=700,
                                 max_features='auto',
                                 oob_score=True,
                                 random_state=1,
                                 n_jobs=-1)
    
    rf.fit(train_data, train_target1)
    predictions = rf.predict_proba(test_data)
    
    predictions_data=[]
    
    for i in range(0,len(predictions)):
        predictions_data.append(predictions[i][1])
    
    test_target["credibility"] = predictions_data
    test_target.columns=["questionAnswer_id","credibility_new"]
    connection = pymysql.connect(host='192.168.160.36', port=3306, user='user_zwb', password='123456', db='grammer',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql1="SELECT * FROM questionAnswer"
    cursor.execute(sql1)
    connection.commit()
    result = cursor.fetchall()
    feedback_result=[]
    for data in result:
        feedback_result.append(data)
    feedback_result=pd.DataFrame(feedback_result)
    feedback_to_target=feedback_result[["questionAnswer_id","credibility"]]
    for i in range(0,len(test_target)):
        try:
            sql = "UPDATE questionAnswer SET credibility = {1} WHERE questionAnswer_id='{2}'".format(str(test_target.loc[i,'credibility_new']),str(test_target.loc[i,'questionAnswer_id']))
            cursor.execute(sql)
            connection.commit()
        except:
            connection.rollback()
    connection.close()
    return(1)

if __name__ == '__main__':
    data_all = wide_table_maker()
    print(question_score(data_all))