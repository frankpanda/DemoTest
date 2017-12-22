#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import json
import csv
import os

# 预发布环境
HOST_GATEWAY = "http://116.62.26.185:8100"
HOST_SXT = "http://120.26.244.205:8092"
pwd = "Ze48Lq7/iiHPtyAtsopZfw=="
session = requests.session()


def get_response_data(server=None, uri=None, method=None, params=None, data=None, headers=None):
    """
    获取请求接口的响应值
    :param server:
    :param uri: 接口uri
    :param params: 提交参数
    :param data: 提交参数
    :param method: 请求方法GET/POST
    :param headers:自定义header
    :return: 服务器响应数据
    """
    if server.lower() == "gateway":
        url = HOST_GATEWAY + uri
    elif server.lower() == "sxt":
        url = server + uri
    else:
        print server
        print "please input a right server name..."
        return ""

    # 发送请求
    if method.lower() == "get":
        response_data = session.get(url, params=json.dumps(params), headers=headers)
    elif method.lower() == "put":
        response_data = session.put(url, params=json.dumps(params), data=json.dumps(data), headers=headers)
    elif method.lower() == "post":
        response_data = session.post(url, params=json.dumps(params), data=json.dumps(data), headers=headers)

    return response_data.status_code, response_data.text


def get_params_from_csv(csv_path, cols_no=0):
    """
    引用的文件为已经生成好的数据文件，格式为：getaccountid,usercccount,gettokenid
    :param csv_path:读取文件路径
    :param cols_no:数据行号：第一列getaccountid,第二列usercccount,第三列gettokenid
    :return:
    """
    with open(csv_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        if cols_no == 0:
            data = [row for row in reader]
        else:
            data = [row[cols_no - 1] for row in reader]

    return data


def create_data():
    login_uri = "/uic/api/auth/login/cipher"

    # 创建txt数据文件
    test_data_path = r"e:/test_data_debug.txt"
    account_file_path = r"e:/studata_debug.txt"
    if os.path.exists(test_data_path):
        os.remove(test_data_path)
    test_data_file = open(test_data_path, "a")

    # 获取登录token
    headers = {
        "Content-Type": "application/json",
        "ACCEPT": "*/*",
        "Connection": "close",
        "charset": "UTF-8"
    }

    # 计数器
    counter = 0
    for account in open(account_file_path, "r"):
        data = {'userType': 1, 'client': 2, 'account': account.strip(), 'password': pwd, 'clientIdentity': ''}
        response_info = get_response_data(login_uri, "POST", data=data, headers=headers)
        if response_info[0] != 200:
            continue
        else:
            try:
                res_data_dict = json.loads(response_info[1])
            except Exception, e:
                print u"Json处理异常..."
                print response_info[1]
                print e

            token_value = res_data_dict["data"]["token"]

        print token_value


if __name__ == "__main__":
    pass
