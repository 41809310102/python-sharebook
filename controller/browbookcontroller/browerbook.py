import datetime
import json
from functools import wraps

from flask import Blueprint, request, render_template, make_response

from utils import create_sql, mybaits

api_url_brobook = Blueprint('/brobook', __name__)


@api_url_brobook.route('/page')
def get_page():
    return render_template("forstudent.html")


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    return wrapper_fun


@api_url_brobook.route('/browbooks/addbro', methods=['POST', 'GET'])
@allow_cross_domain
def get_addbro():
    bid = request.form['bid']
    uid = request.form['uid']
    bt_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 先判断当前是否可借
    sql4 = "select brownum from book where id={}".format(str(bid))
    res_bro = mybaits.select(sql4, ['brownum'])
    if res_bro[0]['brownum'] == 0:
        res_data = {
            'code': -1,
            'msg': "该图书暂无余量，请联系管理员！"
        }
        return res_data

    sql1 = create_sql.create_selectbyid(['id'], ['uid', 'bid'], 'brower',
                                        ['{}'.format(str(uid)), '{}'.format(str(bid))])
    res = mybaits.select(sql1, ['id'])
    if len(res) > 0:
        res_data = {
            'code': -1,
            'msg': "你已经借阅过该书，请勿重复借阅"
        }
    else:
        sql = create_sql.create_insert(['uid', 'bid', 'bk_time', 'state'],
                                       ["{}".format(str(uid)), "{}".format(str(bid)), "'{}'".format(bt_time),
                                        "{}".format("0")], 'brower')
        res = mybaits.add(sql)
        if res > 0:
            res_data = {
                'code': 1,
                'msg': "借阅成功"
            }
            # 成功后将书籍的借阅数量减一
            sql = "update book set brownum = brownum-1 WHERE `id` = {}".format(str(bid))
            mybaits.update(sql)
        else:
            res_data = {
                'code': 1,
                'msg': "借阅失败"
            }
    return json.dumps(res_data).encode('utf-8')
