# 2. 爬取电影天堂 主页中的 最新发布180部影视 的每一部电影的详细信息

import requests
from lxml import etree

link = "https://www.dytt8.net"
# 存储电影的详细信息
Movies_information = []
# 存储电影的url
Movie_url = []
# 记录电影奖的集合
flag = ['奥斯卡', '金球奖', '金鸡奖', '百花奖', '金马奖', '香港电影金像奖', '柏林电影节金熊奖']
# User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36',
    'Referer': 'https://www.dytt8.net'
}


# 根据url获取html
def getHtml(url):
    res = requests.get(url, headers=headers)
    # 从网页的内容中分析网页编码的方式
    res.encoding = res.apparent_encoding
    return res.text


# 获取一页的电影url
def getallpage_url(page):
    html = etree.HTML(page)
    urls = html.xpath("//div[@class = 'co_content8']//ul//table//a/@href")
    Movie_url.extend(list(map(lambda url: link + url, urls)))


# 获取电影详情
def get_movie_detail(url):
    movie = {}
    page = getHtml(url)
    html = etree.HTML(page)
    # 获取电影名称
    title = html.xpath("//h1/font[@color = '#07519a']/text()")[0]
    movie["title"] = title
    # 获取全部的信息
    content = html.xpath("//div[@id = 'Zoom']//text()")
    # 获取各项信息
    movie['create_local'] = content[5]
    movie['up_year'] = title[:5]

    if str(content[6]).find('类') == -1:
        movie['type'] = content[5]
    else:
        movie['type'] = content[6]

    if str(content[8]).find('豆瓣评分') != -1:
        movie['douban_grade'] = content[8]
        movie['time_total'] = content[9]
    elif str(content[9]).find('豆瓣评分') != -1:
        movie['douban_grade'] = content[9]
        movie['time_total'] = content[10]
    elif str(content[10]).find('豆瓣评分') != -1:
        movie['douban_grade'] = content[10]
        movie['time_total'] = content[11]
    elif str(content[11]).find('豆瓣评分') != -1:
        movie['douban_grade'] = content[11]
        movie['time_total'] = content[12]
    else:
        # 如果没有爬取到，给一个默认值
        movie['douban_grade'] = "◎豆瓣评分\u30006.0/10 from 8530  users"
        movie['time_total'] = "◎片\u3000\u3000长\u3000120分"
    # movie['time_total'] = content[10]
    content_str = str(content)
    for data in flag:
        if content_str.find(data) != -1:
            print(content_str)
    # movie["information"] = content_str.encode().decode('utf-8')
    Movies_information.append(movie)


# range(1, 20)从第一页爬取到第20页
def parse_HTML():
    for i in range(1, 20):
        url = "https://www.dytt8.net/html/gndy/dyzz/list_23_" + str(i) + ".html"
        page = getHtml(url)
        getallpage_url(page)
    for index, url in enumerate(Movie_url):
        if index >= 180:
            break
        get_movie_detail(url)
        print(Movies_information[index])
    saveData()


# 保存数据
def saveData():
    # 写入txt文件
    with open('moviesky.txt', 'w', encoding='utf-8') as f:
        for movie_info in Movies_information:
            str1 = str(movie_info) + '\n'
            f.write(str1)
        f.close()


# 电影天堂数据爬取主程序
if __name__ == '__main__':
    print("正在连接网站中.........")
    parse_HTML()
    print("爬取结束.........")
