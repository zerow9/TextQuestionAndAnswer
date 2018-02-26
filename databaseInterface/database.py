#!/usr/bin/env python
# !coding:utf-8

import pymysql
import uuid
import time

def connectDataBase(host, user, password, database, port):
    try:
        connect = pymysql.connect(host=host, user=user, password=password, db=database, port=port, charset='utf8')
        cursor = connect.cursor()
        return connect, cursor
    except Exception as e:
        print(e.args)

class Database(object):
    def __init__(self,host,user,password,database,port=3306):
        '''
        :param host:数据库IP地址
        :param user: 链接数据库用户名
        :param password: 链接数据库密码
        :param db: 需要链接的数据库
        :param port: 链接数据库端口
        '''
        self.host = host
        self.user = user
        self.passwd = password
        self.database = database
        self.port = port
        self.connect,self.cur = connectDataBase(self.host,self.user,self.passwd,self.database,self.port)
    # '''-----------------------------------增------------------------------------------------'''
    def insertDataArticle(self,ownUser,articleName,articlePath):
        '''
        插入数据到文章表
        :param ownUser:文件上传者
        :param articleName: 文件名称
        :param articlePath: 文件存储的位置
        article_id:文件编号
        :return:
        '''
        articleId = str(uuid.uuid1()).replace('-','')
        try:
            articleName = articleName.replace('\\', '/').split('/')[-1]
            sql = '''insert into article(article_id,own_user,article_name,article_path) VALUES ("%s",%d,"%s","%s")'''
            self.cur.execute(sql%(articleId,ownUser,articleName,articlePath))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def insertDataBaiduResult(self,ownArticle,sentence,baiduResult):
        '''
        插入数据到百度API结果表
        :param ownArticle: 所属文章ID
        :param sentence:句子
        :param baiduResult:百度API返回的结果
        baiduResultId:百度API存储结果ID
        :return:
        '''
        baiduResultId = str(uuid.uuid1()).replace('-','')
        try:
            ownArticle = ownArticle.replace('\\', '/').split('/')[-1]
            sql = '''insert into baiduResult(baiduResult_id,own_article,sentence,baiduResult) VALUES ("%s","%s","%s","%s")'''
            self.cur.execute(sql%(baiduResultId,ownArticle,sentence,baiduResult))
            self.connect.commit()
            return baiduResultId
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def insertDataQuestionAnswer(self,ownArticle,fromProduce,question,answer):
        '''
        插入数据到问题答案键值对表
        :param fromProduce: 来自哪条百度API结果
        :param ownArticle:句子所属文章
        :param question: 问题
        :param answer: 答案
        questionAnswer_id:键值对ID
        produce_time: 键值对产生的时间

        :return:
        '''
        questionAnswerId = str(uuid.uuid1()).replace('-','')
        produceTime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            ownArticle = ownArticle.replace('\\', '/').split('/')[-1]
            sql = '''insert into questionAnswer(questionAnswer_id,own_article,from_produce,question,answer,produce_time) VALUES ("%s","%s","%s","%s","%s","%s")'''
            self.cur.execute(sql%(questionAnswerId,ownArticle,fromProduce,question,answer,produceTime))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    # '''-----------------------------------删------------------------------------------------'''
    def deleteDataArticle(self,articleId):
        '''
        删除文章，关联删除文章中的句子所得到的百度API返回结果，关联删除文章所产生的问题答案键值对
        :param articleId: 文章ID
        :return:
        '''
        try:
            sql = '''delete from questionAnswer WHERE own_article="%s"'''
            self.cur.execute(sql % (articleId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)
        try:
            sql = '''delete from baiduResult WHERE own_article="%s"'''
            self.cur.execute(sql % (articleId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)
        try:
            sql = '''delete from article where article_id="%s"'''
            self.cur.execute(sql%(articleId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def deleteDataBaiduResult(self,baiduResultId):
        '''
        删除百度API返回结果，关联删除根据该百度API所生成的问题答案键值对
        :param baiduResultId: 百度API结果ID
        :return:
        '''
        try:
            sql = '''delete from questionAnswer WHERE from_produce="%s"'''
            self.cur.execute(sql % (baiduResultId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)
        try:
            sql = '''delete from baiduResult WHERE baiduResult_id="%s"'''
            self.cur.execute(sql % (baiduResultId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def deleteDataQuestionAnswer(self,questionAnswerId):
        '''
        删除问题答案键值对
        :param questionAnswerId:问题答案键值对ID
        :return:
        '''
        try:
            sql = '''delete from questionAnswer WHERE questionAnswer_id="%s"'''
            self.cur.execute(sql % (questionAnswerId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    # '''-----------------------------------改------------------------------------------------'''
    def updateDataArticle(self,articleId,**kwargs):
        '''
        根据文章ID更新文章表
        :param articleId:需要修改的文章ID
        :param kwargs:
            own_user：文章上传者
            article_name：文章名称
            article_path：文章存储路径
            article_sentences_number：文章中间结果
        :return:
        '''
        try:
            sql = '''UPDATE article SET '''
            for key in kwargs:
                sql+='''%s=%s,'''%(key,kwargs[key])
            sql = sql[:-1]+''' where article_id="%s"'''%(articleId)
            # sql = '''UPDATE article SET WHERE article_id="%s" '''
            self.cur.execute(sql)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def updateDataBaiduResult(self,baiduResultId,**kwargs):
        '''
        根据百度API返回结果ID更新百度API返回结果表
        :param baiduResultId:需要修改的百度API ID
        :param kwargs:
            own_article:句子所属文章
            sentence：句子
            baiduResult：百度API返回结果
        :return:
        '''
        try:
            sql = '''UPDATE baiduResult SET '''
            for key in kwargs:
                sql+='''%s=%s,'''%(key,kwargs[key])
            sql = sql[:-1]+''' where baiduResult_id="%s"'''%(baiduResultId)
            self.cur.execute(sql)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    def updateDataQuestionAnswer(self,questionAnswerId,**kwargs):
        '''
        根据问题答案键值对ID更新问题答案键值对表
        :param questionAnswerId:需要修改的问题答案键值对ID
        :param kwargs:
            own_article:所属文章
            from_produce：百度API结果
            question：问题
            answer：答案
            produce_time：键值对产生时间
            yes_or_no：是否合理问题
            form_user：确认用户
            commit_time：确认时间
        :return:
        '''
        commitTime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql = '''UPDATE questionAnswer SET '''
            for key in kwargs:
                sql+='''%s=%s,'''%(key,kwargs[key])
            sql += ''' commit_time="%s" where questionAnswer_id="%s"'''%(commitTime,questionAnswerId)
            # sql = '''UPDATE article SET WHERE article_id="%s" '''
            self.cur.execute(sql)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e.args)

    # '''-----------------------------------查------------------------------------------------'''
    def selectDataArticleAll(self,start=0,page=10):
        '''
        查询所有的文章列表的所有信息
        :param start:开始，表示从第几条信息开始，默认从第一条开始（0）
        :param page:大小，表示一页显示多少条数据，默认一页显示10条信息
        :return:所有的文章列表信息
        '''
        data = []
        sql = 'select * from article limit %d,%d'
        self.cur.execute(sql%(start,page))
        for key in self.cur.fetchall():
            data.append(key)
        return data

    def selectDataArticleByArticleName(self,articleName):
        '''
        根据文章名称查询文章ID
        :param articleName:文章名称
        :return:文章ID
        '''
        sql = '''select article_id from article WHERE article_name="%s"'''
        self.cur.execute(sql % (articleName.replace('\\','/').split('/')[-1]))
        data = self.cur.fetchall()
        if len(data)>0:
            return data[0][0]
        else:
            return None

    def selectDataArticleUser(self,ownUser,start=0,page=10):
        '''
        根据上传者查询所有文章，查询当前用户上传的所有文章的所有信息
        :param ownUser:文章上传者ID
        :param start:开始，表示从第几条信息开始，默认从第一条开始（0）
        :param page:大小，表示一页显示多少条数据，默认一页显示10条信息
        :return:当前用户上传的所有文章的所有信息
        '''
        data = []
        sql = '''select * from article WHERE own_user="%s" limit %d,%d '''
        self.cur.execute(sql%(ownUser,start,page))
        for key in self.cur.fetchall():
            data.append(key)
        return data

    def selectDataBaiduResult(self,sentence):
        '''
        根据句子查询百度API结果
        :param sentence: 句子
        :return: 百度API结果
        '''
        try:
            sql = '''SELECT baiduResult,baiduResult_id FROM baiduResult WHERE sentence="%s"'''
            self.cur.execute(sql%(sentence))
            return self.cur.fetchall()
        except Exception as e:
            print(e.args)

    def selectDataQuestionAnswerAll(self,start=0,page=10):
        '''
        查询所有的问题答案键值对信息
        :param start:开始，表示从第几条信息开始，默认从第一条开始（0）
        :param page:大小，表示一页显示多少条数据，默认一页显示10条信息
        :return:所有答案问题键值对
        '''
        data = []
        sql = 'select * from questionAnswer limit %d,%d'
        self.cur.execute(sql%(start,page))
        for key in self.cur.fetchall():
            data.append(key)
        return data

    def selectDataQuestionAnswerYes(self,yesOrNo=1,start=0,page=10):
        '''
        查询合理/不合理问题
        :param yesOrNo:合理/不合理问题，默认为1（合理），否则为0（不合理）
        :param start:开始，表示从第几条信息开始，默认从第一条开始（0）
        :param page:大小，表示一页显示多少条数据，默认一页显示10条信息
        :return:所有答案问题键值对
        '''
        data = []
        sql = 'select * from questionAnswer where yes_or_no=%d limit %d,%d'
        self.cur.execute(sql%(yesOrNo,start,page))
        for key in self.cur.fetchall():
            data.append(key)
        return data

    def selectDataQuestionAnswerArticle(self,articleId,start=0,page=10):
        '''
        根据文章查询
        查询指定文章对应的所有问题答案键值对信息
        :param articleId:文章ID
        :param start:开始，表示从第几条信息开始，默认从第一条开始（0）
        :param page:大小，表示一页显示多少条数据，默认一页显示10条信息
        :return:所有答案问题键值对
        '''
        data = []
        sql = '''select * from questionAnswer WHERE own_article="%s" limit %d,%d'''
        self.cur.execute(sql%(articleId,start,page))
        for key in self.cur.fetchall():
            data.append(key)
        return data

    def selectDataQuestionAnswerUser(self,user,start=0,page=10):
        '''
        根据文章查询
        查询指定文章对应的所有问题答案键值对信息
        :param start:开始，表示从第几条信息开始，默认从第一条开始（0）
        :param page:大小，表示一页显示多少条数据，默认一页显示10条信息
        :param user:确认用户ID
        :return:所有答案问题键值对
        '''
        data = []
        sql = '''select * from questionAnswer WHERE form_user="%d" limit %d,%d'''
        self.cur.execute(sql%(user,start,page))
        for key in self.cur.fetchall():
            data.append(key)
        return data
