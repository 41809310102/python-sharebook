class Type(object):
    def __init__(self):
        self.typeid = None
        self.typename = None

    def get_typeid(self):
        return self.typeid

    def get_typename(self):
        return self.typename

    def set_typeid(self, value):
        self.typeid = value

    def set_typename(self, value):
        self.typename = value

