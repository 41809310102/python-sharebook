# 用户登陆类

class Book(object):
    def __init__(self):
        self.id = 0
        self.title = ""
        self.douban = ""
        self.type = ""
        self.country = ""
        self.uptime = ""
        self.time_total = ""

    def getMovie_id(self):
        return self.id

    def getMovie_name(self):
        return self.title

    def getMovie_douban(self):
        return self.douban

    def getMovie_type(self):
        return self.type

    def getMovie_country(self):
        return self.country

    def getMovie_uptime(self):
        return self.uptime

    def getMovie_time_total(self):
        return self.time_total

    def setMovie_id(self, value):
        self.id = value

    def setMovie_title(self, value):
        self.title = value

    def setMovie_douban(self, value):
        self.douban=value

    def setMovie_type(self, value):
        self.type = value

    def setMovie_country(self, value):
        self.country = value

    def setMovie_uptime(self, value):
        self.uptime = value

    def setMovie_time_total(self, value):
        self.time_total  = value
