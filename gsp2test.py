#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import hashlib
import time
import datetime
import json
from datetime import datetime

import logging
from xlrd import xldate_as_tuple
import requests
import xlrd
import os
import sys
import re
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'Frank_Xiong'


# MD5加密字符串
def md5(string):
    """
    把字符串转化成MD5值
    :param string:
    :return:
    """
    if not isinstance(string, str):
        string = str(string)
    m = hashlib.md5()
    m.update(string)

    return m.hexdigest()


# 获取签名
def get_sign(appkey, app_secret, excel_json_dict):
    """
    获取签名
    :param app_secret:
    :param appkey:
    :param excel_json_dict:从excel文件中获取的参数字典
    :return:返回签名字符串
    """
    params_dict = get_sign_param_dict(excel_json_dict)
    params_list = [app_secret]
    params_dict["appkey"] = appkey
    # logging.info(u"-----遍历参数-----")
    try:
        for key in sorted(params_dict.keys()):
            param_value = params_dict.get(key)
            # logging.debug(param_value)
            if not isinstance(param_value, str):
                if isinstance(param_value, dict) or isinstance(param_value, unicode):
                    param_value = str(param_value)
                else:
                    print param_value
                    param_value = str(int(param_value))
            print param_value, type(param_value)
            params_list.append(key + param_value.strip())
    except Exception, e:
        print u"拼接参数异常..."
        print e

    params_list.append(app_secret)
    # 把参数列表转换成字符串
    params_string = "".join(params_list)
    print "签名加密前：", params_string

    # MD5加密
    params_md5 = md5(params_string)
    sign_str = params_md5.upper()
    print sign_str

    return sign_str


def get_login_token_value(url, appkey):
    """
    获取登录接口返回的token值
    :return:
    """
    login_r = requests.post(url, data={"appkey": appkey})
    # 获取响应json
    # print u"响应数据:", login_r.text
    json_dict = login_r.json()
    if json_dict["code"] == 0:
        # 从请求响应内容中获取token值
        token = json_dict["data"]["access_token"]
        # print "token:", token
        return token
    else:
        print u"获取token失败..."
        return ""


def get_timestamp():
    """
    获取时间戳
    :return:
    """
    current_timestamp = int(time.time())
    return current_timestamp


def get_http_header(appkey, params_sign, login_url):
    """
    组装http请求的header
    :param appkey: 接口的appkey
    :param params_sign: 参数签名
    :param login_url: 登录接口的url
    :return: 返回组装好的header字典
    """
    headers_dict = {
        "token": get_login_token_value(login_url, appkey),
        "appkey": appkey,
        "format": "json",
        "timestamp": str(get_timestamp()),
        "sign": params_sign
    }

    return headers_dict


def get_data_from_excel(excel_path, caseid):
    """
    从excel文件中根据caseid读取数据生成robotframework测试用例需要的各种数据
    :param excel_path: excel文件路径
    :param caseid: 测试用例的id
    :return:返回运行用例所需参数字典
    """
    # 读取excel文件
    data = xlrd.open_workbook(excel_path.decode("utf-8"))
    # 获取第一张表单
    sheet = data.sheets()[0]
    # 获取总行数和总列数
    # rows_total = sheet.nrows
    cols_total = sheet.ncols
    # 把excel中的前两行标题去除
    caseid_list = sheet.col_values(0)[2:]
    # 获取excel文件第一行的标题，参数名除外
    title_list = sheet.row_values(0)
    print U"打印标题列表:%s" % title_list
    # 获取caseid所在行
    try:
        caseid_in_row = caseid_list.index(caseid) + 2
    except ValueError, e:
        logging.info(u"在excel文件中没有找到%s,请确认caseid是否正确！" % caseid)
        logging.info(e)
    # 定义用例的数据字典
    case_data_json = dict()
    case_name = u"%s_%s" % (caseid, sheet.cell(caseid_in_row, title_list.index("case_name")).value)
    case_data_json["case_name"] = case_name
    case_data_json["http_method"] = sheet.cell(caseid_in_row, title_list.index("http_method")).value
    case_data_json["uri"] = sheet.cell(caseid_in_row, title_list.index("uri")).value
    case_data_json["setup_sql_path"] = sheet.cell(caseid_in_row, title_list.index("setup_sql_path")).value
    case_data_json["teardown_sql_path"] = sheet.cell(caseid_in_row, title_list.index("teardown_sql_path")).value
    case_data_json["expected"] = sheet.cell(caseid_in_row, title_list.index("expected")).value

    # 判断是否有path，如果有则组装path参数字典
    if "path" in title_list:
        begin_index_path = title_list.index("path")
        for title in title_list[begin_index_path + 1:]:
            if title != "":
                # path参数结束列索引值
                end_index_path = title_list.index(title)
                break
        print u"end_index_path:%d" % end_index_path

        # 定义保存path参数的字典
        path_dict = dict()
        for i in range(begin_index_path, end_index_path):
            path_key = sheet.cell(1, i).value
            path_value = convert_value_type(sheet.cell(caseid_in_row, i).value, sheet.cell(caseid_in_row, i).ctype)
            path_dict[path_key] = path_value

        case_data_json["path"] = path_dict

        # 处理uri中的参数
        uri_no_params = replace_param_in_path(case_data_json["uri"], path_dict)
        case_data_json["uri"] = uri_no_params

        print u"打印path字典:"
        print path_dict
        print U"处理完成后不带参数的uri: %s" % case_data_json["uri"]

    # 判断是否有params参数，如果有则组装成参数字典
    if "params" in title_list:
        begin_index_params = title_list.index("params")
        for title in title_list[begin_index_params + 1:]:
            if title != "":
                end_index_params = title_list.index(title)
                break
        print u"end_index_param:%d" % end_index_params

        # 定义保存params参数的字典
        params_dict = dict()
        for i in range(begin_index_params, end_index_params):
            param_key = sheet.cell(1, i).value
            param_value = convert_value_type(sheet.cell(caseid_in_row, i).value, sheet.cell(caseid_in_row, i).ctype)
            if isinstance(param_value, unicode):
                # 判断该参数是否需要从其他sheet引用数据组装成json或者List
                if "[" in param_value or "{" in param_value:
                    param_value = get_json_param_from_sheet(data, param_value)

            params_dict[param_key] = param_value

        case_data_json["params"] = params_dict

    # 判断是否有data参数，如果有则组装成参数字典
    if "data" in title_list:
        begin_index_data = title_list.index("data")
        for title in title_list[begin_index_data + 1:]:
            if title != "":
                end_index_data = title_list.index(title)
                break
        print u"end_index_data:%d" % end_index_data

        # 定义保存data参数的字典
        data_dict = dict()
        for i in range(begin_index_data, end_index_data):
            data_key = sheet.cell(1, i).value
            data_value = convert_value_type(sheet.cell(caseid_in_row, i).value, sheet.cell(caseid_in_row, i).ctype)
            if isinstance(data_value, unicode):
                # 判断该参数是否需要从其他sheet引用数据组装成json或者List
                if "[" in data_value or "{" in data_value:
                    data_value = get_json_param_from_sheet(data, data_value)

            data_dict[data_key] = data_value

        case_data_json["data"] = data_dict

    print json.dumps(case_data_json)
    return case_data_json


def get_json_param_from_sheet(xlrd_data, param_value):
    """
    从sheet表单中获取数据组装成list或者json
    :param xlrd_data: xlrd读取excel文件对象
    :param param_value: 测试用例数据参数值
    :return:组装好的json或者list
    """
    sheet_name = param_value[1:-1]

    sheet = xlrd_data.sheet_by_name(sheet_name)
    # 获取标题列关键字
    key_list = sheet.row_values(0)
    # 获取行数和列数
    row_num = sheet.nrows
    col_num = sheet.ncols
    # 参数值是列表
    if "[" in param_value:
        param_data = []
        for row in range(1, row_num):
            temp_dict = dict()
            for col in range(col_num):
                dict_value = convert_value_type(sheet.cell(row, col).value, sheet.cell(row, col).ctype)
                if isinstance(dict_value, unicode):
                    # 判断测试数据里面是否有特殊标志
                    if "[" in dict_value or "{" in dict_value:
                        temp_dict[key_list[col]] = get_json_param_from_sheet(xlrd_data, dict_value)
                    else:
                        temp_dict[key_list[col]] = dict_value
                else:
                    temp_dict[key_list[col]] = dict_value

            param_data.append(temp_dict)
    else:
        # 参数值是字典
        param_data = dict()
        for col in range(col_num):
            dict_value = convert_value_type(sheet.cell(1, col).value, sheet.cell(1, col).ctype)
            if isinstance(dict_value, unicode):
                # 判断测试数据里面是否有特殊标志
                if "[" in dict_value or "{" in dict_value:
                    param_data[key_list[col]] = get_json_param_from_sheet(xlrd_data, dict_value)
                else:
                    param_data[key_list[col]] = dict_value
            else:
                param_data[key_list[col]] = dict_value

    return param_data


def replace_param_in_path(uri_str, path_dict):
    """
    利用正则去匹配替换uri里面的参数
    :param uri_str: 需要处理的带参数的uri
    :param path_dict: 用户替换的path参数字典
    :return: 处理完的uri
    """
    find_list = re.findall("{\w+}", uri_str)
    for item in find_list:
        uri_str = re.sub(item, str(path_dict[item[1:-1]]), uri_str)

    return uri_str


def get_sign_param_dict(excel_json_dict):
    """
    生成接口签名所需的参数字典
    :param excel_json_dict:从excel文件中读取出的参数字典
    :return:返回组装好的参数字典
    """
    sign_dict = dict()
    sign_dict["format"] = "json"
    sign_dict["timestamp"] = get_timestamp()

    if "path" in excel_json_dict:
        sign_dict.update(excel_json_dict["path"])
    if "params" in excel_json_dict:
        sign_dict.update(excel_json_dict["params"])
    if "data" in excel_json_dict:
        sign_dict.update(excel_json_dict["data"])

    return sign_dict


def convert_value_type(cell_value, value_type):
    """
    根据excel表中值类型把读取到的excel值转换成正确的值
    :param cell_value: 从excel表中读取到的值
    :param value_type: excel中的值类型
    0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    :return:转换后的值
    """
    if value_type == 2:
        if cell_value != int(cell_value):
            return cell_value
        else:
            return int(cell_value)
    elif value_type == 3:
        # 转换成常见的日期格式
        date = datetime(*xldate_as_tuple(cell_value, 0))
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(time_array))
    else:
        return cell_value


def create_testcase(file_path, dest_path):
    """
    生成RF的测试用例
    path可以为excel文件路径，也可以为excel所在文件夹路径，如果是文件夹路径则会降里面所有excel文件生成测试用例；如果是excel文件路径则只生成改excel的测试用
    :param file_path: excel所在目录或者excel文件路径
    :param dest_path: 保存生成RF用例文件的路径
    :return:
    """
    # print chardet.detect(file_path)
    if not os.path.exists(file_path):
        print u"请确认该文件或者目录是否正确：%s" % file_path.decode("utf-8")
        return
    else:
        if os.path.isdir(file_path):
            # 获取文件列表
            file_list = os.listdir(file_path)
            for file_name in file_list:
                if os.path.isfile(os.path.join(file_path + "/" + file_name)):
                    if is_excel(file_name):
                        # 拼接excel文件的完整路径
                        full_excel_path = file_path + "/" + file_name
                        create_rffile_by_excel(full_excel_path, dest_path)
        else:
            create_rffile_by_excel(file_path, dest_path)

    print u"所有用例生成完成。"


def is_excel(file_name):
    """
    根据文件后缀名判断该文件是否是excel文件
    :param file_name:文件名
    :return:
    """
    name_tuple = os.path.splitext(file_name)
    if name_tuple[-1] == ".xls" or name_tuple[-1] == ".xlsx":
        return True
    else:
        # print type(file_name), chardet.detect(file_name)
        print u"[%s]不是excel文件，请确认！" % file_name.decode("gb2312")
        return False


def create_rffile_by_excel(excel_file_path, dest_path):
    """
    通过读取excel文件中的数据生成RF详细测试套件txt文件
    :param excel_file_path: excel文件的路径
    :param dest_path: 生成RF用例文件保存目录
    :return: None
    """
    if not os.path.exists(dest_path):
        print "dest_path", dest_path, type(dest_path), chardet.detect(dest_path)
        os.mkdir(dest_path)

    # 读取excel文件中的caseid
    data = xlrd.open_workbook(excel_file_path)
    sheet = data.sheet_by_index(0)
    caseid_list = sheet.col_values(0)[2:]
    case_name_list = sheet.col_values(2)[2:]

    # 测试套件文件名
    case_file_name = dest_path + "/" + os.path.basename(excel_file_path).split(".")[0] + ".txt"
    if os.path.exists(case_file_name):
        os.remove(case_file_name)
    # print "case_file_name", case_file_name, type(case_file_name), chardet.detect(case_file_name)
    f = open(case_file_name, "a")
    f.write("""*** Settings ***
Resource          ../utils.txt

*** Test Cases ***
""")
    # 写入测试用例信息
    # print type(os.path.basename(excel_file_path)), chardet.detect(os.path.basename(excel_file_path))
    print u"正在生成[%s]文件的用例..." % os.path.basename(excel_file_path)
    for caseid in caseid_list:
        testcase_full_name = "%s_%s" % (caseid, case_name_list[caseid_list.index(caseid)])
        case_data_dict = get_data_from_excel(excel_file_path, caseid)
        logging.info(u"正在生成测试用例->[%s]" % testcase_full_name)
        f.write(testcase_full_name.encode("utf-8"))
        f.write("\n")
        # 如果该用例的setup_sql_path单元格不为空则写入setup信息；为空则不写入
        if case_data_dict["setup_sql_path"]:
            f.write("""    [Setup]    handle_testdata    %(setup_sql_path)s""" % {"setup_sql_path": case_data_dict["setup_sql_path"].encode("utf-8")})
            f.write("\n")

        f.write("""    exc_request    %(excel_file_path)s    %(caseid)s""" % {"excel_file_path": excel_file_path.encode("utf-8"), "caseid": caseid.encode("utf-8")})
        f.write("\n")

        # 如果该用例的teardown_sql_path单元格内容不为空则写入teardown信息；为空则不写入
        if case_data_dict["teardown_sql_path"]:
            f.write("""    [Teardown]    handle_testdata    %(teardown_sql_path)s""" % {"teardown_sql_path": case_data_dict["teardown_sql_path"].encode("utf-8")})
            f.write("\n")

    f.close()

    print u"[%s]文件的用例生成完成" % os.path.basename(excel_file_path)
    print "##########################################"


def request_http_by_method(server_url, headers, test_data):
    """
    根据不同的请求方式发起不同的请求：get、put、post、delete
    :param server_url:连接服务器的url
    :param headers:定制的header头信息
    :param test_data:从excel读取的测试用例数据字典
    :return 接口响应数据
    """
    url = server_url + test_data["uri"]
    session = requests.session()
    if test_data["http_method"] == "get":
        response = session.get(url, headers=headers, params=test_data.get("params"))
    elif test_data["http_method"] == "post":
        response = session.post(url, headers=headers, params=test_data.get("params"), data=test_data.get("data"))
    elif test_data["http_method"] == "put":
        response = session.put(url, headers=headers, params=test_data.get("params"), data=test_data.get("data"))
    else:
        response = session.delete(url, headers=headers, params=test_data.get("params"))

    return response


if __name__ == "__main__":

    appkey = "automation_007"
    app_secret = "6B8CA4A0177164CC6D5C5DC92222BBC2"
    login_url = "http://test.gsp2.chinawayltd.com/api/user/auth"
    main_url = "http://test.gsp2.chinawayltd.com/api"

    from_excel_dict = get_data_from_excel(r"d:/automation/orders_year_list.xlsx", "TESTCASE001")
    sign = get_sign(appkey, app_secret, from_excel_dict)
    header = get_http_header(appkey, sign, login_url)

    response_data = request_http_by_method(main_url, header, from_excel_dict)
    print response_data.text
    print response_data.url

    # create_testcase("d:/automation", "d:/automation/testcase")
    # get_data_from_excel("d:/automation/order_detail.xlsx", "TESTCASE001")
