class Student(object):
    def __init__(self):
        self.name = None
        self.password = None

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def set_name(self, value):
        self.name = value

    def set_password(self, value):
        self.password = value

