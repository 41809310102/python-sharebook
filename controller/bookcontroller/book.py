import json

from flask import Blueprint, render_template, request

from dao.Book import Book
from dao.Student import Student
from utils import mybaits, create_sql
from utils.page import create_page

api_url_book = Blueprint('booklist', __name__)


@api_url_book.route('/list', methods=['POST', 'GET'])
def get_list():
    arr_select = []
    print(len(request.args))
    if len(request.args) > 2:
        name = request.args['bookname']
        actor = request.args['author']
        typeid = request.args['typeid']
        sql = create_sql.create_select(['*'], ['name', 'actor'], 'book',
                                       ['"%{}%"'.format(name), '"%{}%"'.format(actor)])
    else:
        sql = create_sql.create_select(['*'], ['name', 'actor'], 'book', ['"%{}%"'.format(""), '"%{}%"'.format("")])
    res = mybaits.select(sql, ['id', 'name', 'actor', 'createtime', 'state', 'pic', 'downurl', 'brownum', 'typename',
                               'desction', 'typeid', 'publisher'])
    page = request.args['page']
    limit = request.args['limit']
    res = create_page(int(page), int(limit), res)
    res_data = {
        "code": 0,
        "msg": "",
        "count": len(res),
        "data": res
    }
    return json.dumps(res_data).encode('utf-8')


@api_url_book.route('book/addOrUpdateBook', methods=['POST', 'GET'])
def get_add():
    book = Book()
    data = request.form
    print(data)
    book.set_name("'{}'".format(data['name']))
    book.set_pic("'{}'".format(data['pic']))
    book.set_downurl("'{}'".format(data['pic']))
    book.set_actor("'{}'".format(data['actor']))
    book.set_createtime("'2022-12-18'")
    book.set_brownum(data['brownum'])
    book.set_state(data['state'])
    book.set_publisher("'{}'".format(data['publisher']))
    book.set_desction("'{}'".format(data['desction']))
    book.set_typeid(data['typeid'])
    book.set_typename("'{}'".format(get_type(data['typeid'])))
    print(book.get_typename())
    res = mybaits.add(
        create_sql.create_insert(
            ['name', 'pic', 'actor', 'createtime', 'brownum', 'downurl', 'typeid', 'desction', 'publisher', 'state',
             'typename'],
            [book.get_name(), book.get_pic(), book.get_actor(),
             book.get_createtime(),
             book.get_brownum(), book.get_downurl(), book.get_typeid(), book.get_desction(), book.get_publisher(),
             book.get_state(), book.get_typename()], "book"))
    print(book.get_typename())
    if res == 1:
        return "success"
    else:
        return "fail"


@api_url_book.route('/search', methods=['POST', 'GET'])
def get_search():
    return ""


@api_url_book.route('book/delBook', methods=['POST', 'GET'])
def get_del():
    id = request.args['id']
    sql = create_sql.create_del(['id'], 'book', id)
    mybaits.deledb(sql)
    return "删除成功!"


@api_url_book.route('/bookpage', methods=['POST', 'GET'])
def get_page():
    return render_template("book.html")


@api_url_book.route('book/getAllType', methods=['POST', 'GET'])
def get_all_type():
    sql = create_sql.create_select(['*'], ['typeid', 'typename'], 'typedb', ['"%{}%"'.format(""), '"%{}%"'.format("")])
    print(sql)
    res = mybaits.select(sql, ['typeid', 'typename'])
    return json.dumps(res).encode('utf-8')


def get_type(id):
    sql = create_sql.create_select(['*'], ['typeid', 'typename'], 'typedb', ['"%{}%"'.format(id), '"%{}%"'.format("")])
    res = mybaits.select(sql, ['typeid', 'typename'])
    return res[0]['typename']

