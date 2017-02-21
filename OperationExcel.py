#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'Huoyunren'

import xlwt


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


if __name__ == "__main__":
    get_data_excel()
    # get_data_csv()
