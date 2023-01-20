class Brower(object):
    def __init__(self):
        self.id = None
        self.uid = None
        self.bid = None
        self.bk_time = None
        self.state = None

    def get_id(self):
        return self.id

    def get_uid(self):
        return self.uid

    def get_bid(self):
        return self.bid

    def get_bk_time(self):
        return self.bk_time

    def get_state(self):
        return self.state

    def set_id(self, value):
        self.id = value

    def set_uid(self, value):
        self.uid = value

    def set_bid(self, value):
        self.bid = value

    def set_bk_time(self, value):
        self.bk_time = value

    def set_state(self, value):
        self.state = value

    def get_classinfo(self):
        res = ['id', 'uid', 'bid', 'bk_time', 'state']
        return res