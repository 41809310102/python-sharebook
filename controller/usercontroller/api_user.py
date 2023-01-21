import datetime
import json
import os

from dao import success
from flask import Blueprint, request
from mapper import userMapper
from flask import render_template
from dao.User import User
from utils import create_sql, mybaits
from utils.page import create_page

api_url_user = Blueprint('/', __name__)


# 用户个人主页
@api_url_user.route('/myinfo')
def get_myinfo():
    return render_template("myinfo.html")


# 用户列表
@api_url_user.route('/list', methods=['POST', 'GET'])
def get_list():
    if request.method == "GET":
        username = request.args['username']
        if username != "null":
            password = request.args['password']
            sex = request.args['sex']
            root = request.args['root']
        else:
            return render_template("userlist.html")
            # 查询是否存在该用户账号
        res = userMapper.select_user_have(username)
        create_time = str(datetime.datetime.now())
        user = User()
        user.setuser_password(password)
        user.setuser_name(username)
        user.setuser_sex(sex)
        user.setuser_root(root)
        user.setuser_createtime(create_time)
        if res['id'] != 0:
            user.setuser_id(res['id'])
            userMapper.update_info(user)
        else:
            userMapper.add_user(user)
    return render_template("userlist.html")


# 用户登陆接口
@api_url_user.route("/login", methods=['POST', 'GET'])
def login():
    username = request.args['username']
    password = request.args['password']
    res = userMapper.select_userisok(username, password)
    print(res)
    if res['code'] != 0:
        return success.res(res['user'], 1, "登陆成功")
    else:
        return success.res("", -1, "登陆失败，请检查用户名密码")


# 用户注册逻辑
@api_url_user.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        root = request.form['root']
        # 查询是否存在该用户账号
        res = userMapper.select_userisok(username, password)
        if res['code'] != 0:
            return success.res(res, 2, "当前存在该账户，请勿重复注册")
    else:
        username = request.args['username']
        password = request.args['password']
        sex = request.args['sex']
        root = request.args['root']
    create_time = str(datetime.datetime.now())
    user = User()
    user.setuser_password(password)
    user.setuser_name(username)
    user.setuser_sex(sex)
    user.setuser_root(root)
    user.setuser_createtime(create_time)
    res = userMapper.add_user(user)
    if res != 0:
        return success.res("", 1, "注册成功")
    else:
        return success.res("", -1, "注册失败，请稍后重试")


# 用户修改密码
@api_url_user.route("/update/information", methods=['POST', 'GET'])
def updateInformation():
    # 验证密码是否正确
    # TODO 查库
    # 如果密码正常，支持修改
    # TODO 改库
    # 确认修改成功
    if True:
        return success.res("", 1, "账号修改成功")
    else:
        return success.res("", -1, "账号修改失败，请重新尝试")


# 管理员权限设置
"""
  id:id序号
  root：角色1代表普通用户，角色2代表管理员
"""


# 权限修改
@api_url_user.route("/update/root", methods=['POST', 'GET'])
def updata_root():
    # 将对应的id人员的root字段改为设置的角色字段
    if True:
        return success.res("", 1, "权限修改成功")
    else:
        return success.res("", -1, "账号权限修改失败，请重新尝试")


# 列表维护
@api_url_user.route("/user_list", methods=['POST', 'GET'])
def get_userlist():
    page = request.args['page']
    limit = request.args['limit']
    list = userMapper.select_User("-1", "")
    res = create_page(int(page), int(limit), list)
    res_data = {
        "code": 0,
        "msg": "",
        "count": len(list),
        "data": res
    }
    return json.dumps(res_data).encode('utf-8')


# 模糊搜索
@api_url_user.route("/sreach_list", methods=['POST', 'GET'])
def get_userlist_sreach():
    page = request.args['page']
    limit = request.args['limit']
    username = request.args['username']
    ids = request.args['id']
    print("ids", ids)
    if ids != '':
        list_res = userMapper.select_User(str(ids), username)
        res = create_page(int(page), int(limit), list_res)
        res_data = {
            "code": 0,
            "msg": "",
            "count": len(list_res),
            "data": res
        }
    else:
        list_res = userMapper.select_User("-1", username)
        res = create_page(int(page), int(limit), list_res)
        res_data = {
            "code": 0,
            "msg": "",
            "count": len(list_res),
            "data": res
        }
    return json.dumps(res_data).encode('utf-8')


@api_url_user.route("/del_user", methods=['POST', 'GET'])
def del_user():
    id = request.args['id']
    userMapper.del_user(str(id))
    res = {
        'code': 1,
        'msg': "删除成功"
    }
    return json.dumps(res).encode("utf-8")


@api_url_user.route("/update_info", methods=['POST', 'GET'])
def info_user():
    id = request.form['id']
    username = request.form['username']
    sign = request.form['sign']
    sex = request.form['sex']
    res_data = userMapper.user_info(id, username, sign, sex)
    if res_data == 1:
        res = {
            'code': 1,
            'msg': "修改成功，请退出登陆，查看信息"
        }
    else:
        res = {
            'code': 0,
            'msg': "修改失败，请重新尝试"
        }
    return json.dumps(res).encode("utf-8")


@api_url_user.route("/update_info_pass", methods=['POST', 'GET'])
def info_user_pass():
    id = request.form['id']
    username = request.form['username']
    oldpassword = request.form['oldpas']
    newpassword = request.form['newpas']
    res_isok = userMapper.select_userisok(username, oldpassword)
    if res_isok['code'] != 0:
        res_pass = userMapper.user_info_pass(id, username, newpassword)
        if res_pass == 1:
            res = {
                'code': 1,
                'msg': "修改成功，请退出登陆"
            }
        else:
            res = {
                'code': 0,
                'msg': "修改失败，请重新尝试"
            }
    else:
        res = {
            'code': 0,
            'msg': "旧密码核验不成功！请重新输入"
        }
    return json.dumps(res).encode("utf-8")


# 我的借阅
@api_url_user.route("/mybook", methods=['POST', 'GET'])
def get_mybook():
    return render_template("mybook.html")


# 查询我的借阅历史

@api_url_user.route('/admin/mybrower', methods=['POST', 'GET'])
def get_all_bro():
    uid = request.args['uid']
    sql = create_sql.create_selectbyid(['*'], ['uid'], 'brower', ["{}".format(str(uid))])
    res = mybaits.select(sql, ['id', 'uid', 'bid', 'bk_time', 'state'])
    # 处理说明较长的图书
    res_book = []
    if len(res) > 0:
        for k in res:
            sql_book = create_sql.create_selectbyid(['name', 'actor', 'pic', 'publisher'], ['id'], 'book',
                                                    ['{}'.format(k['bid'])])
            res_data = mybaits.select(sql_book, ['name', 'actor', 'pic', 'publisher'])

            node = res_data[0]
            node['bk_time'] = k['bk_time']
            node['state'] = k['state']
            node['bid'] = k['bid']
            res_book.append(node)
        res_data = {
            'code': 1,
            'data': res_book,
            'msg': "success"
        }
    else:
        res_data = {
            'code': -1,
            'data': res_book,
            'msg': "您当前没有借阅历史，请前往借阅再来偶！"
        }
    return json.dumps(res_data).encode('utf-8')


# 归还图书
@api_url_user.route('admin/guihuan', methods=['POST', 'GET'])
def get_guihuan():
    uid = request.args['uid']
    bid = request.args['bid']
    sql = "update brower  set  state = 1 where uid={}".format(str(uid)) + " and bid={}".format(str(bid))
    mybaits.update(sql)  # 处理说明较长的图书
    res_data = {
        'code': 1,
        'msg': "归还成功！"
    }
    return json.dumps(res_data).encode('utf-8')


# 删除图书
@api_url_user.route('admin/del_book', methods=['POST', 'GET'])
def get_del_book():
    uid = request.args['uid']
    bid = request.args['bid']
    sql = create_sql.create_del_more(['uid', 'bid'], 'brower', ['{}'.format(str(uid)), '{}'.format(str(bid))])
    mybaits.deledb(sql)
    # 处理说明较长的图书
    res_data = {
        'code': 1,
        'msg': "删除成功！"
    }
    return json.dumps(res_data).encode('utf-8')


# 我的分享
@api_url_user.route("/myshare", methods=['POST', 'GET'])
def get_myshare():
    return render_template("myshare.html")


# 资源上传
@api_url_user.route("/update_txt", methods=['POST', 'GET'])
def get_update_txt():
    """
           文件上传
       """
    if request.method == 'POST':
        # input标签中的name的属性值
        f = request.files['file']
        # 拼接地址，上传地址，f.filename：直接获取文件名
        str_s = get_by_id()
        f.save(os.path.join("bookzip/booktxt/", "{}.txt".format(str_s)))
        # 输出上传的文件名
        print(request.files, f.filename)
        res = {
            'code': 1,
            'msg': '文件上传成功!',
            'id': str_s
        }
        return json.dumps(res).encode('utf-8')
    else:
        return render_template('myshare.html')


# 封面上传
@api_url_user.route("/update_img", methods=['POST', 'GET'])
def get_update_img():
    """
           文件上传
       """
    if request.method == 'POST':
        # input标签中的name的属性值
        f = request.files['file']
        # 拼接地址，上传地址，f.filename：直接获取文件名
        f.save(os.path.join("static/img/book/", f.filename))
        # 输出上传的文件名
        print(request.files, f.filename)
        res = {
            'code': 1,
            'msg': '封面上传成功!',
            'src': "../img/book/{}".format(f.filename)
        }
        return json.dumps(res).encode('utf-8')
    else:
        return render_template('myshare.html')


# 获取当前信息数据
def get_by_id():
    sql = "select id from sharebook where id>0 order by id desc limit 1"
    res = mybaits.select(sql, ['id'])
    if len(res) == 0:
        return "1"
    else:
        return str(res[0]['id'] + 1)


# 添加分享的书籍到数据库中
@api_url_user.route("/addbook", methods=['POST', 'GET'])
def add_sharebook():
    title = request.form['title']
    ids = request.form['id']
    pic = request.form['img']
    myname = request.form['myname']
    actor = request.form['actor']
    sql = create_sql.create_insert(['title', 'pic', 'actor', 'share_name', 'state'],
                                   ["'{}'".format(title), "'{}'".format(pic), "'{}'".format(actor),
                                    "'{}'".format(myname), "'1'"], 'sharebook')
    res = mybaits.add(sql)
    if res > 0:
        res_data = {
            'code': 1,
            'msg': "分享成功"
        }
    else:
        res_data = {
            'code': 1,
            'msg': "分享失败"
        }

    return json.dumps(res_data).encode('utf-8')


if __name__ == '__main__':
    get_by_id()
