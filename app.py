import json

from flask import Flask, render_template

from controller.bookcontroller.book import api_url_book
from controller.bookcontroller.searchbook import api_url_books
from controller.browbookcontroller.browerbook import api_url_brobook
from controller.moviecontroller.api_file import api_url_movie
from controller.usercontroller.api_user import api_url_user


app = Flask(__name__)

movice = []

app = Flask(import_name=__name__,
            static_url_path='',  # 配置静态文件的访问url前缀
            static_folder='static',  # 配置静态文件的文件夹
            template_folder='templates')  # 配置模板文件的文件夹


# 加载爬取的网站数据
def read_file():
    with open("service/moviesky.txt", "r", encoding="utf-8") as f:  # 打开文件
        line = f.readline()  # 调用文件的 readline()方法，一次读取一行
        while line:
            res = eval(str(line))
            movice.append(res)
            line = f.readline()
        f.close()


@app.route('/lay.html')
def moban():
    return render_template("lay.html")


# 统计电影类别数
@app.route('/chart/mydata')
def get_mov_type():
    read_file()
    type_list = ['喜剧', '爱情', '剧情', '惊悚', '动作', '奇幻', '战争', '动画', '冒险']
    data_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for obj in movice:
        for t in type_list:
            if str(obj['type']).find(t) != -1:
                if t == '喜剧':
                    data_count[0] = data_count[0] + 1
                if t == '爱情':
                    data_count[1] = data_count[1] + 1
                if t == '剧情':
                    data_count[2] = data_count[2] + 1
                if t == '惊悚':
                    data_count[3] = data_count[3] + 1
                if t == '动作':
                    data_count[4] = data_count[4] + 1
                if t == '奇幻':
                    data_count[5] = data_count[5] + 1
                if t == '战争':
                    data_count[6] = data_count[6] + 1
                if t == '动画':
                    data_count[7] = data_count[7] + 1
                if t == '冒险':
                    data_count[8] = data_count[8] + 1
    res = {'喜剧': data_count[0],
           '爱情': data_count[1],
           '剧情': data_count[2],
           '惊悚': data_count[3],
           '动作': data_count[4],
           '奇幻': data_count[5],
           '战争': data_count[6],
           '动画': data_count[7],
           '冒险': data_count[8]}
    # Address = Count_Flag_And_Flow("d://access_log")
    return render_template("mydata.html", data=json.dumps(res))


# 统计豆瓣评分分数个数
@app.route('/chart/read_file')
def get_grade():
    res = {
        'code': -1
    }
    num1 = 0  # 大于8分
    num2 = 0  # 大于7分小于8分
    num3 = 0  # 大于6分小于7分
    num4 = 0  # 大于5分小于6分
    num5 = 0  # 大于3分小于5分
    num6 = 0  # 小于3分
    for k in movice:
        data = str(k['douban_grade'])
        start = data.find('.') - 1
        end = start + 3
        grade = float(data[start:end])
        if grade >= 8.0:
            num1 += 1
        elif 7.0 <= grade < 8.0:
            num2 += 1
        elif 6.0 <= grade < 7.0:
            num3 += 1
        elif 5.0 <= grade < 6.0:
            num4 += 1
        elif 3.0 <= grade < 5.0:
            num5 += 1
        else:
            num6 += 1

    name_type = ['大于8分', '大于7分小于8分', '大于6分小于7分', '大于5分小于6分', '大于3分小于5分', '小于3分']
    data_value = [num1, num2, num3, num4, num5, num6]
    res = {
        'code': 0,
        'data': name_type,
        'value': data_value
    }

    return json.dumps(res).encode('utf-8')


# 分析2018-2022年电影发布数量
@app.route('/chart/year')
def get_year_num():
    res = {
        'code': -1
    }
    year_name = ['2018年', '2019年', '2020年', '2021年', '2022年']
    data_value = [0, 0, 0, 0, 0]
    for obj in movice:
        for k in year_name:
            if str(obj['up_year']).find(k):
                if k == '2018年':
                    data_value[0] = data_value[0] + 1
                if k == '2019年':
                    data_value[1] = data_value[1] + 1
                if k == '2020年':
                    data_value[2] = data_value[2] + 1
                if k == '2021年':
                    data_value[3] = data_value[3] + 1
                if k == '2022年':
                    data_value[4] = data_value[4] + 1
    res = {
        'code': -1,
        'data': year_name,
        'value': data_value
    }
    return json.dumps(res).encode('utf-8')


# 分析电影产地
@app.route('/chart/country')
def get_year_country():
    res = {
        'code': -1
    }
    country_name = ['中国', '美国', '法国', '德国', '韩国', '日本', '英国', '西班牙', '荷兰']
    data_value = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for country in movice:
        start = 0
        for k in country_name:
            if str(country['create_local']).find(k) != -1:
                data_value[start] = data_value[start] + 1
                start = 0
            else:
                start += 1
    res = {
        'code': -1,
        'data': country_name,
        'value': data_value
    }
    return json.dumps(res).encode('utf-8')


# 统计电影时长
@app.route('/chart/time')
def get_time():
    res = {
        'code': -1
    }
    count_data = [0, 0, 0, 0, 0]
    for time_node in movice:
        datas = str(time_node['time_total'])
        time_long = 0
        if datas.find('片') != -1:
            len_node = len(datas)
            end = str(datas).find('分')
            start = str(datas).find('长') + 2
            try:
                time_long = int(datas[start:end])
            except:
                time_long = 90  # 筛选错误，默认为90
        else:
            time_long = 90
            # 开始统计时长
        if time_long < 60:
            count_data[0] += 1
        elif 60 <= time_long < 90:
            count_data[1] += 1
        elif 90 <= time_long < 120:
            count_data[2] += 1
        elif 120 <= time_long < 150:
            count_data[3] += 1
        else:
            count_data[4] += 1
    time_name = ['<60分钟', '60-90分钟', '90-120分钟', '120-150分终', '>150分钟']
    pie_node = {
        'name': time_name[0],
        'value': count_data[0]
    }
    pie_node1 = {
        'name': time_name[1],
        'value': count_data[1]
    }
    pie_node2 = {
        'name': time_name[2],
        'value': count_data[2]
    }
    pie_node3 = {
        'name': time_name[3],
        'value': count_data[3]
    }
    pie_node4 = {
        'name': time_name[4],
        'value': count_data[4]
    }
    res = {
        'code': 1,
        'data': [pie_node, pie_node1, pie_node2, pie_node3, pie_node4]
    }
    return json.dumps(res).encode('utf-8')


# 首页
@app.route('/')
def login():
    return render_template("login.html")


# 注册页面
@app.route('/register')
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.register_blueprint(api_url_user, url_prefix='/admin')
    app.register_blueprint(api_url_movie, url_prefix='/film')
    app.register_blueprint(api_url_book, url_prefix='/book')
    app.register_blueprint(api_url_books, url_prefix='/searchpage')
    app.register_blueprint(api_url_brobook,url_prefix='/browbooks')
    app.run('0.0.0.0', port=5001, debug=False)
