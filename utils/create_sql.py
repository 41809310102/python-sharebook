def create_select(prev_list, next_list, table_name, data):
    str_code = "select "
    len_k = len(prev_list)
    for k in range(0, len_k - 1):
        str_code = str_code + prev_list[k] + ","
    str_code = str_code + prev_list[len_k - 1] + " "
    str_code = str_code + "from " + table_name
    if len(next_list) > 0:
        str_code = str_code + " where "
    len_l = len(next_list)
    for k in range(0, len_l - 1):
        str_code = str_code + "{}".format(next_list[k]) + " like " + str(data[k]) + " and "
    str_code = str_code + "{}".format(next_list[len_l - 1]) + " like " + str(data[len_l - 1])
    return str_code


def create_selectbyid(prev_list, next_list, table_name, data):
    str_code = "select "
    len_k = len(prev_list)
    for k in range(0, len_k - 1):
        str_code = str_code + prev_list[k] + ","
    str_code = str_code + prev_list[len_k - 1] + " "
    str_code = str_code + "from " + table_name
    if len(next_list) > 0:
        str_code = str_code + " where "
    len_l = len(next_list)
    for k in range(0, len_l - 1):
        str_code = str_code + "{}".format(next_list[k]) + "=" + str(data[k]) + " and "
    str_code = str_code + "{}".format(next_list[len_l - 1]) + "=" + str(data[len_l - 1])
    print(str_code)
    return str_code


def create_del(next_list, table_name, data):
    str_code = "DELETE FROM " + table_name + " where "
    for k in next_list:
        str_code = str_code + "{}".format(k) + "=" + str(data)
    return str_code


def create_del_more(prev_list, table_name, data):
    str_code = "DELETE FROM " + table_name + " where "
    len_del = len(prev_list)
    print(len_del)
    for k in range(0, len_del - 1):
        str_code = str_code + "{}".format(prev_list[k]) + "=" + str(data[k])+" and "
    str_code += "{}".format(prev_list[len_del-1]) + "=" + str(data[len_del-1])
    return str_code


def create_insert(prev_list, data, table_name):
    str_code = "insert into " + table_name + " ("
    len_k = len(prev_list)
    for k in range(0, len_k - 1):
        str_code = str_code + prev_list[k] + ","
    str_code = str_code + prev_list[len_k - 1] + ") values ("
    for k in range(0, len_k - 1):
        str_code = str_code + str(data[k]) + ","
    str_code = str_code + str(data[len_k - 1]) + ")"

    print(str_code)
    return str_code


def create_update(table_name, prev_list, prev_data, where_list, data):
    str_code = "update " + table_name + " set "
    len_k = len(prev_list)
    for k in range(0, len_k - 1):
        str_code = str_code + prev_list[k] + "=" + prev_data[k] + ","
    str_code = str_code + prev_list[len_k - 1] + "=" + prev_data[len_k - 1] + " where {}".format(where_list[0]) + "=" + str(data)
    return str_code


def create_db(table_name, object_class):
    sql = "create table {}(".format(table_name) + "\n"
    sql += "id int not null auto_increment primary key," + "\n"
    dists = object_class.get_classinfo()
    len_k = len(dists)
    for k in range(1, len_k - 1):
        sql += "{} varchar(30),".format(dists[k]) + "\n"
    sql += "{} varchar(30))".format(dists[len_k - 1]) + "\n"
    return sql


if __name__ == '__main__':
    create_select(['*'], ["id"], "user", 1)
    create_del(['id'], "user", 1)
    create_insert(['name', 'password'], "user", ['1', '123456'])
