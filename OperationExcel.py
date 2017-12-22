#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'Huoyunren'

import xlwt
import xlrd


# excel文件
def get_data_excel():
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("gpsno")
    worksheet.write(0, 0, label="设备号")  # 写标题栏

    gpsno_head = "840"
    # 自动生成10000个设备号
    for i in xrange(1, 50):
        gpsno = gpsno_head + str(i).zfill(5)
        worksheet.write(i, 0, label=gpsno)

    workbook.save(u"D:/批量导入smart设备模板.xls")


# 批量导入smart设备测试数据
def get_data_csv():
    try:
        data = open(u"D:/GSP/Doing/终端列表批量导入/批量导入smart设备模板.csv", "w")
        data.write(u"\"设备卡号\"".encode("utf-8") + "\n")
        gpsno_head = u"\"840a\""
        num = 0
        # 自动生成设备号
        print u"正在生成数据..."
        for i in xrange(30012, 31012):
            gpsno = gpsno_head.replace("a", str(i).zfill(5))
            data.write(gpsno + "\n")
            num += 1

        print u"生成数据完成，共%d条数据。" % num
    except Exception, e:
        print u"生成数据失败：", e
    finally:
        data.close()


def read_merged_cells():
    """
    获取合并单元格的信息
    :return:
    """
    try:
        # xls文件
        # data = xlrd.open_workbook(r"alarm.xls", formatting_info=True)
        # xlsx文件
        data = xlrd.open_workbook(r"d:/automation/demo.xlsx")
    except IOError, e:
        print u"读取文件异常..."
        print e
    sh = data.sheets()[0]
    print u"读取第一张表..."
    print type(sh)
    """
    for crange in sh.merged_cells:
        print u"crange内容:", crange

    if sh.merged_cells is []:
        print u"kong de"
    else:
        print u"not kong"
    """
    print sh.merged_cells
    print sh.nrows
    print sh.cell(0, 3).value

    print "############################"
    print sh.row_values(1)


def get_testcase_from_excel(excel_path):
    """
    从excel文件中读取数据生成robotframework测试用例
    由于excel表中格式固定，所以可以很容易的读取出想要字段，具体表格格式见模板文件
    :param excel_path: excel文件路径
    :return:
    """
    # 读取excel文件
    data = xlrd.open_workbook(excel_path)
    # 获取第一张表单
    sheet = data.sheets()[0]
    # 获取总行数
    rows_count = sheet.nrows
    print sheet.cell(0, 5).value
    print sheet.row_values(0)
    print sheet.row_values(1)
    print sheet.ncols


def test(substring, deststring):
    """
    要在字符串中，查找多个子串是否存在，并打印出这些串和首次出现的位置
    :param substring:
    :param deststring:
    :return:
    """
    return ",".join([str([deststring.index(x), x]) for x in substring if x in deststring])


if __name__ == "__main__":
    get_testcase_from_excel(r"d:/automation/demo.xlsx")
