import time

import pymysql
import config
from utils import create_sql


def connectdb():
    # 打开数据库连接
    try:
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        db = pymysql.connect(host=config.MYSQL_DB_URL['host'], user=config.MYSQL_DB_URL['username'],
                             password=config.MYSQL_DB_URL['password'], database=config.MYSQL_DB_URL['database'])
    except Exception as e:
        print(e)
    return db


# 关闭数据连接
def closedb(db):
    db.close()


# 支持模糊查询
def select(sql, name_list):
    # 使用cursor()方法获取操作游标
    db = connectdb()
    cursor = db.cursor()
    list_data = []
    len_size = len(name_list)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录数量
        num1 = cursor.fetchall()
        list_data = []
        if len(num1) > 0:
            for row in num1:
                node = {}
                for k in range(0, len_size):
                    node[name_list[k]] = row[k]
                list_data.append(node)

        else:
            return list_data
    except:
        print("获取失败！")
    return list_data


# 添加
def add(sql):
    db = connectdb()
    cursor = db.cursor()
    num = cursor.execute(sql)
    print('添加成功')
    db.commit()  # 提交数据
    return num


# 用户信息修改
def update(sql):
    db = connectdb()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        print('信息修改成功')
        db.commit()  # 提交数据
    except:
        print('信息修改失败')
        db.rollback()
        cursor.close()
        db.close()


# 用户信息删除
def deledb(sql):
    db = connectdb()
    cursor = db.cursor()
    print(sql)
    try:
        cursor.execute(sql)
        print("删除数据成功")
        db.commit()  # 提交数据
    except:
        db.rollback()
        cursor.close()
        db.close()


# 创建对象表
def create_table(sql):
    db = connectdb()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        print("创建表成功")
        db.commit()  # 提交数据
    except:
        db.rollback()
        cursor.close()
        db.close()
