import json.decoder


def res(data, code, msg):
    data_res = {
        'code': -1,
        'data': "",
        'msg': "fail"
    }

    if code == 1:
        data_res['data'] = data
    data_res['code'] = code
    data_res['msg'] = msg
    return json.dumps(data_res).encode("utf-8")
