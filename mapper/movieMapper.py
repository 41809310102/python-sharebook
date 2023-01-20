import time

import pymysql
import config



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
def select_Movie(id, title):
    # 使用cursor()方法获取操作游标
    print("开始查询")
    db = connectdb()
    cursor = db.cursor()
    title = "\'%" + title + "%\'"
    if id != "-1":
        sql = "SELECT a.id,a.title,a.douban,b.typename,a.country,a.uptime,a.time_total" \
              " FROM moviedb as a, movietype as b  where  a.id=" + id + " and a.title like " + title + " and a.type=b.id "
    else:
        sql = "SELECT a.id,a.title,a.douban,b.typename,a.country,a.uptime,a.time_total" \
              " FROM moviedb as a, movietype as b  where" + " a.title like " + title + " and a.type=b.id "
    list = []
    try:
        # 执行SQL语句
        print(sql)
        cursor.execute(sql)
        # 获取所有记录数量
        num1 = cursor.fetchall()
        list = []
        if len(num1) > 0:
            for row in num1:
                node = {'id': row[0], 'title': row[1], 'douban': row[2], 'type': row[3], 'country': row[4],
                        'uptime': row[5], 'time_total': row[6]}
                list.append(node)
        else:
            return list
    except:
        print("获取失败！")
    return list


# 检验是否修改或添加
def select_Movie_have(title):
    db = connectdb()
    title = "\"" + title + "\""
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "SELECT id FROM  moviedb WHERE title=" + title
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录数量
        num1 = cursor.fetchall()
        if len(num1) > 0:
            res = {
                'id': num1[0][0],
            }
        else:
            res = {
                'id': 0,
            }
        return res
    except:
        print("数据库连接失败")
    # 上报到管理平台
    closedb(db)


"moviedb.userdb (password,username,root,createtime,sex)"


# 添加电影
def add_Movie(Movie):
    db = connectdb()
    title = "\"" + Movie.getMovie_name() + "\""
    douban = "\"" + Movie.getMovie_douban() + "\""
    uptime = "\"" + Movie.getMovie_uptime() + "\""
    country = "\"" + Movie.getMovie_country() + "\""
    type = "\"" + str(Movie.getMovie_type()) + "\""
    time_total = "\"" + str(Movie.getMovie_time_total()) + "\""
    cursor = db.cursor()
    sql = "insert into moviedb (title,douban,uptime,country,type,time_total) " + "values (" + title + "," + \
          douban + "," + uptime + "," + country + "," + type + "," + time_total + ")"
    num = cursor.execute(sql)
    print('添加成功')
    db.commit()  # 提交数据
    return num


# 用户信息修改
def update_info(Movie):
    db = connectdb()
    cursor = db.cursor()
    title = "\"" + Movie.getMovie_name() + "\""
    douban = "\"" + Movie.getMovie_douban() + "\""
    uptime = "\"" + Movie.getMovie_uptime() + "\""
    country = "\"" + Movie.getMovie_country() + "\""
    type =str(Movie.getMovie_type())
    id = str(Movie.getMovie_id())
    update = "update moviedb  set  title=" + title + ",douban=" + douban + ",country=" + country + \
             ",uptime=" + uptime + ",type=" + type + " where id=" + id
    print(update)
    try:
        cursor.execute(update)
        print('信息修改成功')
        db.commit()  # 提交数据
    except:
        print('信息修改失败')
        db.rollback()
        cursor.close()
        db.close()


# 用户信息删除
def del_Movie(id):
    db = connectdb()
    cursor = db.cursor()
    try:
        update = "DELETE FROM moviedb" + " where id=" + id
        cursor.execute(update)
        print("删除数据成功")
        db.commit()  # 提交数据
    except:
        db.rollback()
        cursor.close()
        db.close()

# 亲空数据库
def del_all_Movie():
    db = connectdb()
    cursor = db.cursor()
    try:
        update = "DELETE FROM moviedb" + " where id>1"
        cursor.execute(update)
        print("电影数据清空成功")
        db.commit()  # 提交数据
    except:
        db.rollback()
        cursor.close()
        db.close()


def add_type(data):
    db = connectdb()
    cursor = db.cursor()
    typename = "\"" + data + "\""
    # 执行SQL语句
    sql = "insert into movietype (typename) values (" + typename + ")"
    try:
        num = cursor.execute(sql)
        print('添加成功')
        db.commit()  # 提交数据
        return num
    except:
        print("数据库连接错误")
    db.rollback()
    cursor.close()
    db.close()
    return 0


if __name__ == '__main__':
    select_Movie("-1", "")
