class Sharebook(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.pic = None
        self.actor = None
        self.state = None
        self.share_name = None

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_pic(self):
        return self.pic

    def get_actor(self):
        return self.actor

    def get_state(self):
        return self.state

    def get_share_name(self):
        return self.share_name

    def set_id(self, value):
        self.id = value

    def set_title(self, value):
        self.title = value

    def set_pic(self, value):
        self.pic = value

    def set_actor(self, value):
        self.actor = value

    def set_state(self, value):
        self.state = value

    def set_share_name(self, value):
        self.share_name = value

    def get_classinfo(self):
        res = ['id', 'title', 'pic', 'actor', 'state', 'share_name']
        return res