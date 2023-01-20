# 用户登陆类

class User(object):
    def __init__(self):
        self.id = 0
        self.username = ""
        self.password = ""
        self.sex = ""
        self.root = 1
        self.createtime = ""
        self.sign = ""

    def getuser_id(self):
        return self.id

    def getuser_sign(self):
        return self.sign

    def getuser_name(self):
        return self.username

    def getuser_password(self):
        return self.password

    def getuser_sex(self):
        return self.sex

    def getuser_root(self):
        return self.root

    def getuser_createtime(self):
        return self.createtime

    def setuser_id(self, value):
        self.id = value

    def setuser_name(self, value):
        self.username = value

    def setuser_password(self, value):
        self.password = value

    def setuser_sex(self, value):
        self.sex = value

    def setuser_root(self, value):
        self.root = value

    def setuser_createtime(self, value):
        self.createtime = value

    def setuser_sign(self, value):
        self.sign = value