# 用户列表
import json
from flask import Blueprint, request
from flask import render_template
from dao import Movie
from mapper import movieMapper
from utils.page import create_page

api_url_movie = Blueprint('movic', __name__)


@api_url_movie.route('/list', methods=['POST', 'GET'])
def get_list():
    if request.method == "GET":
        title = request.args['title']
        if title != "null":
            uptime = request.args['uptime']
            country = request.args['country']
            douban = request.args['douban']
            type = request.args['type']
        else:
            return render_template("booksreach.html")
            # 查询是否存在该用户账号
        res = movieMapper.select_Movie_have(title)
        movie = Movie()
        movie.setMovie_title(title)
        movie.setMovie_country(country)
        movie.setMovie_douban(douban)
        movie.setMovie_uptime(uptime)
        movie.setMovie_type(type)
        if res['id'] != 0:
            movie.setMovie_id(res['id'])
            movieMapper.update_info(movie)
        else:
            movieMapper.add_Movie(movie)
    return render_template("booksreach.html")


# 模糊搜索
@api_url_movie.route("/sreach_list", methods=['POST', 'GET'])
def get_userlist_sreach():
    page = request.args['page']
    limit = request.args['limit']
    title = request.args['title']
    ids = request.args['id']
    print("ids", ids)
    if ids != '':

        list_res = movieMapper.select_Movie(str(ids), title)
        res = create_page(int(page), int(limit), list_res)
        res_data = {
            "code": 0,
            "msg": "",
            "count": len(list_res),
            "data": res
        }
    else:
        list_res = movieMapper.select_Movie("-1", title)
        res = create_page(int(page), int(limit), list_res)
        res_data = {
            "code": 0,
            "msg": "",
            "count": len(list_res),
            "data": res
        }
    return json.dumps(res_data).encode('utf-8')


# 列表维护
@api_url_movie.route("/movie_list", methods=['POST', 'GET'])
def get_userlist():
    page = request.args['page']
    limit = request.args['limit']
    list = movieMapper.select_Movie("-1", "")
    res = create_page(int(page), int(limit), list)
    res_data = {
        "code": 0,
        "msg": "",
        "count": len(list),
        "data": res
    }
    return json.dumps(res_data).encode('utf-8')


@api_url_movie.route("/del_movie", methods=['POST', 'GET'])
def del_user():
    id = request.args['id']
    movieMapper.del_Movie(str(id))
    res = {
        'code': 1,
        'msg': "删除成功"
    }
    return json.dumps(res).encode("utf-8")
