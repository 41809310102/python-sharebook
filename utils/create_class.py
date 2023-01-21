import codecs
import os

from dao.Brower import Brower
from dao.Sharebook import Sharebook
from dao.User import User
from utils.mybaits import create_table
from utils.create_sql import create_db


def create_class(class_name, dist_data, file_path):
    str_code = "class {}(object):".format(class_name) + "\n"
    str_code = str_code + "    def __init__(self):" + "\n"
    for k in dist_data:
        str_code = str_code + "        self.{} ".format(k) + "= None" + "\n"
    str_code = str_code + "\n"
    for k in dist_data:
        str_code = str_code + "    def get_{}".format(k) + "(self):" + "\n"
        str_code = str_code + "        return self.{}".format(k) + "\n\n"

    for k in dist_data:
        str_code = str_code + "    def set_{}".format(k) + "(self, value):" + "\n"
        str_code = str_code + "        self.{}".format(k) + " = value" + "\n\n"

    str_data = "res = ["
    len_s = len(dist_data)
    for k in range(0, len_s - 1):
        str_data += "'{}', ".format(dist_data[k])
    str_data += "'{}',".format(dist_data[len_s - 1]) + "]"
    str_code = str_code + "    def get_classinfo(self):" + "\n"
    str_code = str_code + "        " + str_data + "\n"
    str_code = str_code + "        return res"

    test_dir = file_path
    if os.path.exists(test_dir):
        f = codecs.open(test_dir, 'w', 'utf-8')
        f.write(str_code)
    else:
        py_create(class_name, str_code)


def py_create(name, code):
    desktop_path = "../dao/"
    full_path = desktop_path + name + '.py'
    file = open(full_path, 'w')
    file.write(code)


if __name__ == '__main__':
    obj = Sharebook()
    create_table(create_db("sharebook", obj))
    # create_class('Sharebook', ['id', 'title', 'pic', 'actor', 'state', 'share_name','typename'], '../dao/Sharebook.py')
    # create_class('', ['id', 'userid', 'movie_name', 'grade'], '../dao/Gradeuser')
