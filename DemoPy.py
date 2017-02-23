# _*_ coding:utf-8 _*_

import MySQLdb
import sys
import os
from collections import deque
import xlrd
import time
import datetime
import json

__author__ = 'Panda'

'''
测试向mysql数据库插入中文乱码问题
'''


def insert_mysql_chinese():
    host = "127.0.0.1"
    user = "root"
    password = "111111"
    database = "testdatabase"
    port = 3306
    eng_remark = "test remark string!1"
    chinese_remark = "测试!"
    insert_sql = "insert into students_info(name,mobilephone,remark) values('frank_xiong','18200590917',%s)"

    try:
        db_conn = MySQLdb.connect(host, user, password, database, port, charset='utf8')
        db_cursor = db_conn.cursor()
        db_cursor.execute(insert_sql, (eng_remark,))
        db_cursor.execute(insert_sql, (chinese_remark,))

        db_conn.commit()
        db_cursor.close()
        db_conn.close()
    except MySQLdb.Error, e:
        print "mysql数据库出错：%s" % e

    print sys.getdefaultencoding()


def backup():
    # 备份源目录
    sour_path = "e:\\test\\demo1"
    # 备份到的路径
    dist_path = "e:\\test_backup\\" + time.strftime("%Y%m%d")
    # 备份文件名
    backup_name = time.strftime("%H%M%S") + ".zip"
    # 备份命令
    backup_command = ""

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)
        print"创建目录成功..."


'''
复习巩固
'''


def fun_test(age, *name, **info):
    """测试函数的多个参数"""
    print "age:", age
    print "name:", name
    print "info:", info

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print "今天日期是：", time.strftime("%Y-%m-%d %H:%M:%S")
    print type(timestamp)


def with_star(**star):
    print "你好%(name)s,今年%(age)s岁！" % star  # 格式化输出参数


def without_star(star):
    print "你好%s,今年%s岁！" % (star["name"], star["age"])


def get_fibs(num):
    fibs = [0, 1]
    for i in range(0, num):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


# 递归求阶乘
def jie_cheng(num):
    if num == 1:
        return 1
    else:
        return num * jie_cheng(num - 1)


# 幂运算
def mi(x, n):
    if n == 0:
        return 1
    else:
        return x * mi(x, n - 1)


# 异常
def get_exception():
    try:
        x = int(raw_input("Please input first number:"))
        y = int(raw_input("please input second number:"))
        result = x / y
        print "%s/%s=%s" % (x, y, result)
    except ZeroDivisionError:
        print "second number can't be zero!"
    except TypeError:
        print "you must input a number, not string!"
    except ValueError:
        print "you must input a number, not string!"


def demo():
    print "\ntest..."
    print type(time.strftime("%Y%m%d"))
    test = "ab" + time.strftime("%Y%m%d")
    if 1 == 1:
        print test

    print time.time()

    name = ["panda", "feng", "han", "wei"]
    age = [29, 27, 27, 28]
    # 测试zip函数
    info = zip(name, age)
    print(info)

    ages = age * 3
    print(ages)

    if not 26 in age:
        age.append(26)
        print "age中添加了26！"

    print "age:%s" % age

    flag = "、"
    names = flag.join(name)
    print "names are: %s" % names

    test_string = "xiongbing"
    print list(test_string)
    print "年龄最大的是:%s" % max(age)
    print "年龄最小的是:%s" % min(age)

    age.sort()
    print "排序后的年龄:%s" % age

    # 元组
    print "把序列转化成元组:", tuple(age)

    # 利用deque实现队列
    print type(age)
    queue = deque(age)
    queue.append(30)
    queue.append(40)
    print "Before age:", queue
    queue.popleft()
    print "after age:", queue

    # 字符串
    print test_string.split("i")
    print test_string.title()
    print test_string.replace("i", "z")
    print test_string
    print test_string[0:5]

    # 字典
    info_dict = {
        "panda": 29,
        "han": 28,
        "feng": 28,
        "wei": 29
    }

    print "方法一："
    for name, age in info_dict.items():
        print "%s's age is %s" % (name, age)

    print "方法二："
    for name in info_dict.keys():
        print "%s's age is %s !" % (name, info_dict[name])

    # 字典排序
    print "按key排序："
    for key in sorted(info_dict.keys()):
        print key, info_dict[key]

    print "按value排序："
    print sorted(info_dict.items(), lambda x, y: cmp(x[1], y[1]))

    print dict(info)

    print "字典info_dict的个数：", info_dict.__len__()


def use_zfill():
    head = "840"
    for i in xrange(1, 22):
        gpsn0 = head + str(i).zfill(5)
        print gpsn0,


def get_excel():
    data = xlrd.open_workbook(u"D:/工程师号码/工程师通讯录1.xlsx")
    table = data.sheets()[0]
    # print table.cell(0, 0).value
    # print int(table.cell(1, 0).value)

    col_values = table.col_values(1)
    row_number = table.nrows
    row = []
    for i in xrange(1, row_number):
        row.append(str(col_values[i]).split(".")[0])
    for x in row:
        print x


def get_sign():
    params = {
        "app_key": 1,
        "method": 2,
        "operator": 3,
        "user_id": 4,
        "channel": 5,
        "content": 6,
        "mobile": 7,
        "timestamp": 8,
        "sign": 9
    }

    # 根据参数名称来排序
    temp_string = ["httx"]
    for key in sorted(params.keys()):
        if not isinstance(params[key], str):
            params[key] = str(params[key])
        temp_string.append(key + params[key])
    temp_string.append("httx")
    param_string = "".join(temp_string)
    print param_string


def get_time():
    seconds = time.time()
    mseconds = long(seconds * 1000)

    print mseconds
    date_time = datetime.datetime.now()
    print date_time
    print long(time.mktime(date_time.timetuple()) * 1000.0 + date_time.microsecond / 1000.0)
    # 事件转毫秒计数
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1474859178))


def handle_json():
    d = {"xing": "xiong", "ming": "bing"}
    # 把其他类型转化成json串
    data = json.dumps(d)
    print type(data)
    # 把json串转化成字典
    data_string = json.loads(data)
    print type(data_string)


def handle_dir_file(path_name):
    '''
    path_name = u"D:/工程师号码/mobile.xls"
    dir_path, file_name = os.path.split(path_name)

    print u"目录：", dir_path
    print u"文件名：", file_name
    '''
    # 遍历目录下的所有文件
    files_list = os.listdir(path_name)
    for f in files_list:
        path = path_name + "/" + f
        if os.path.isdir(path):
            # print u"dir_path = " + path
            handle_dir_file(path)
        else:
            print f


def un_encode(input_string):
    print input_string.decode("utf-8")


def turn_to_diff():
    dict_string = {"name": "panda", "age": 20, "data": {"sex": "male", "address": "test"}}
    print u"转换前：", type(dict_string)
    print dict_string
    str_dict = str(dict_string)
    print u"转换后：", type(str_dict)
    print str_dict
    print str_dict.strip()


def use_sort():
    temp_list = [1, 4, 3, 9, 4, 5]
    after_sorted = sorted(temp_list)
    print temp_list
    print after_sorted
    temp_list.sort()
    print temp_list


def maopao_sort(list_data):
    """
    冒泡排序
    :param list_data:
    :return:
    """

    for i in range(0, len(list_data)):
        for j in range(0, len(list_data) - i - 1):
            if list_data[j] > list_data[j + 1]:
                list_data[j], list_data[j + 1] = list_data[j + 1], list_data[j]
    print list_data


def fibs(num):
    """ use yield keyword """

    n, a, b = 0, 0, 1
    while n < num:
        yield b
        a, b = b, a + b
        n += 1


def use_yield():
    """
    yield的基本用法
    :return:
    """
    print "Hi, i'm before yield!"
    yield 5
    print "hi, i'm after first yield!"
    yield 10


if __name__ == "__main__":
    # demo()
    # use_zfill()
    # get_excel()
    # get_sign()
    # get_time()
    # handle_dir_file(u"D:/主文件夹")
    # un_encode(u"测试")
    # turn_to_diff()

    """
    before_name = "xiong"
    after_name = "bing"
    fun_test(10, "frank", "xiong", mobile="18628286213", sex="male")
    print get_fibs(18)

    args = {"name": "panda", "age": 29}
    with_star(**args)

    del args["name"]
    print args

    print jie_cheng(4)
    print mi(3, 3)

    get_exception()
    """
    # print time.strftime("%Y-%m-%d %H:%M:%S")
    # fun_test(10, "frank", "xiong", mobile="18628286213", sex="male")
    # use_sort()
    # maopao_sort([2, 5, 4, 8, 11, 3, 6])

    y = use_yield()
    print y.next()
    print y.next()
