import json
import os

from flask import Blueprint, request, render_template, Response

from utils import create_sql, mybaits

api_url_books = Blueprint('search', __name__)


# 图书检索
@api_url_books.route('/list', methods=['POST', 'GET'])
def get_page():
    return render_template("booksreach.html")


# 图书检索
@api_url_books.route('book/search', methods=['POST', 'GET'])
def get_all_type():
    name = request.args['book_name']
    sql = create_sql.create_select(['*'], ['name'], 'book',
                                   ['"%{}%"'.format(name)])
    res = mybaits.select(sql, ['id', 'name', 'actor', 'createtime', 'state', 'pic', 'downurl', 'brownum', 'typename',
                               'desction', 'typeid', 'publisher'])
    # 处理说明较长的图书
    res_book = []
    for k in res:
        if len(k['desction']) > 99:
            k['desction'] = k['desction'][:99] + "......"
        res_book.append(k)
    res_data = {
        'code': 1,
        'data': res_book,
    }
    return json.dumps(res_data).encode('utf-8')


# 图书分享页
@api_url_books.route('/share', methods=['POST', 'GET'])
def get_sharebook():
    return render_template("bookshare.html")


@api_url_books.route('book/all_share', methods=['POST', 'GET'])
def get_all_share():
    title = request.args['book_name']
    sql = create_sql.create_select(['*'], ['title'], 'sharebook',
                                   ['"%{}%"'.format(title)])
    res = mybaits.select(sql, ['id', 'name', 'pic', 'actor', 'state', 'share_name', 'typename'])
    # 处理说明较长的图书
    res_book = []
    for k in res:
        if len(k['name']) > 99:
            k['name'] = k['name'][:99] + "......"
        res_book.append(k)
    res_data = {
        'code': 1,
        'data': res_book,
    }
    return json.dumps(res_data).encode('utf-8')


# 图书下载
@api_url_books.route('book/down_book', methods=['POST', 'GET'])
def get_downbook():
    ids = request.args['id']
    down_url = 'bookzip/booktxt/{}.txt'.format(str(ids))
    print(down_url)
    if not os.path.exists(down_url):
        return "下载资源不存在，请联系管理员"  # 这里初始化应该存在ec文件
    with open(down_url, 'rb') as f:
        r = f.read()
        response = Response(r, content_type='application/octet-stream')
        response.headers['Content-disposition'] = 'attachment; filename=%s' % 'book.txt'
    return response
