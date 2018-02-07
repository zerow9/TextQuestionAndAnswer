#!/usr/bin/env python
#!coding:utf-8
import pymysql as mysql
import datetime

# 连接数据库的信息
# conn = mysql.connect(host="192.168.160.36", user="zw", passwd="root", db="ask", charset="utf8")

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def insert_mysql(values):
    """插入数据库"""
    # global values
    questionAnwser = {}
    for (ask,label,anwser,_,_) in values:
        if 'UUID' in label or str(ask).count("-")==4 or str(ask)==str(anwser):
            continue
        if isNumber(ask):
            ask = int(ask)
        ask=str(ask)+"的"+str(label)+'是什么?'
        questionAnwser[ask] = str(anwser)
    return questionAnwser
        # print(ask,"-->"+str(anwser))
    # cur = conn.cursor()
    # sql = "INSERT INTO ask_answer(ask,label,answer,filename,time) VALUES (%s,%s,%s,%s,%s)"
    # cur.executemany(sql, values)
    # conn.commit()
    # cur.close()
    # print("保存完毕！")
    # values.clear()


def bitch_insert(values,ask):
    """批量加入"""
    # global values
    values.append(ask)
    return values


def ergodic_tree(trees, file_name):
    """ 遍历树
    :param trees:  树
    :param file_name:  文件名
    """
    values = []
    if not trees:
        return
    for ask in trees:
        for uuid in trees[ask]:
            _uuid = trees[ask][uuid]
            for label in trees[_uuid]:
                value = trees[_uuid][label]
                if len(str(ask).strip()) == 0 or ("uuid" in label) or len(str(value).strip()) == 0:
                    continue
                else:
                    if len(str(ask)) or len(str(label)) or len(str(value)):
                        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f = (ask, label, value, file_name, dt)
                        bitch_insert(values,f)
    return insert_mysql(values)
