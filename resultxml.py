#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
import xlwt
import os
import sys
import ConfigParser
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'xiong bing'


class ResultData(object):
    """
    该类用于解析jmeter生成的xml文件并提取指定数据写入excel文件中
    """

    def __init__(self):
        self.current_datetime = self.__get_current_datetime()
        self.current_date = self.__get_current_date()
        # 保存pass用例的excel文件路径
        self.excel_path_pass = None
        # 保存failure用例的excel文件路径
        self.excel_path_fail = None
        # 保存所有用例的excel文件路径
        self.excel_path_all = None
        # 保存excel文件的目录地址
        self.result_date_path = None
        cfg_data = ParseConfig()
        self.result_xml_path = cfg_data.get_result_xml_path()
        self.test_plan_name = cfg_data.get_test_plan_name()
        # 所有执行结果数据
        self.all_result_list = self.get_result_data_from_xml()
        # 执行失败的结果数据
        self.failure_result_list = [data for data in self.all_result_list if data[5] == "fail"]
        # 测试结果xml文件本分地址
        self.backup_xml_path = None

    def __get_current_datetime(self):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    def __get_current_date(self):
        return time.strftime('%Y%m%d', time.localtime(time.time()))

    def get_result_xml_path(self):
        return self.result_xml_path

    def get_failure_result(self):
        return self.failure_result_list

    def get_failure_result_num(self):
        return len(self.failure_result_list)

    def get_all_result_num(self):
        return len(self.all_result_list)

    def get_start_time(self):
        return self.all_result_list[0][4]

    def get_end_time(self):
        return self.all_result_list[self.get_all_result_num() - 1][4]

    def get_test_plan_name(self):
        return self.test_plan_name

    def set_backup_xml_path(self, xml_path):
        self.backup_xml_path = xml_path

    def get_backup_xml_path(self):
        return self.backup_xml_path

    @staticmethod
    def convert_timestamp(timestamp):
        """
        把时间戳转换成年月日时分秒格式
        :param self:
        :param timestamp:时间戳
        :return: 日期时间
        """
        time_array = time.localtime(long(str(timestamp)[0:-3]))
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

        return datetime

    def create_excel_path(self, flag_name):
        """
        组装存放excel文件路径名称，并根据flag生成不同的文件名称
        :param flag_name: 需要组装的自定义excel文件名
        :return: excel文件完整路径
        """
        log_path = u"ResultFile/" + self.current_date
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.result_date_path = log_path
        excel_path = log_path + u"/" + flag_name + "_" + self.current_datetime + ".xls"
        return excel_path

    def backup_result_xml(self, xml_path):
        """
        备份jmeter生成的xml文件到excel文件同级目录
        :param xml_path: jmeter生成的xml文件路径，直接从cfg文件中读取
        :return:
        """
        dist_path = self.result_date_path + u"/" + u"TestResult_" + self.current_datetime + u".jtl"
        self.set_backup_xml_path(dist_path)
        try:
            shutil.copyfile(xml_path, dist_path)
            print u"%s文件成功备份到%s" % (xml_path, dist_path)
            print u"正在删除源%s文件..." % xml_path
            os.remove(xml_path)
            print u"成功删除%s文件" % xml_path
        except IOError, e:
            print u"备份xml文件失败，请检查xml文件是否存在..."
            print e

    def write_excel(self, save_type="failure"):
        '''
        从测试结果的xml文件中提取所需数据并保存到excel文件中
        :param save_type: 保存失败或者所有数据到excel文件(failure:失败,all:所有)
        :return:
        '''

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(u"result")
        # 列名
        head_list = [u"接口URL", u'参数', u"用例名", u"耗时(毫秒)", u"执行时间", u"测试结果", u"响应码", u"响应信息", u"断言错误信息", u"响应数据"]
        # 写入标题
        for i in range(len(head_list)):
            worksheet.write(0, i, head_list[i])

        # xml_data_list = self.get_result_data_from_xml()
        print u"开始生成Excel文件..."
        if save_type == "failure":
            row_num = 1
            for result in self.failure_result_list:
                for i in range(len(result)):
                    worksheet.write(row_num, i, result[i])
                row_num += 1
            excel_path = self.create_excel_path(u"TestResult_Failure")
            self.excel_path_fail = excel_path
            workbook.save(excel_path)
        else:
            row_num = 1
            for result in self.all_result_list:
                for i in range(len(result)):
                    worksheet.write(row_num, i, result[i])
                row_num += 1
            excel_path = self.create_excel_path(u"TestResult_All")
            self.excel_path_all = excel_path
            workbook.save(excel_path)

        print u"生成%s文件成功" % os.path.split(excel_path)[1]

    def get_result_data_from_xml(self):
        '''
        从jmeter生成的xml文件中提取需要的关键字信息
        :return: 返回获取到的数据作为列表返回
        '''
        try:
            xml_data = ET.parse(self.result_xml_path)
        except IOError, e:
            print u"请确认%s文件是否存在..." % self.result_xml_path
            print e
            exit(0)
        test_result_root = xml_data.getroot()
        http_samples = test_result_root.findall(u"httpSample")
        # 保存提取到的数据列表
        result_list = []
        print u"开始从xml结果文件中提取数据..."
        for sample in http_samples:
            data_list = []
            # data_list列表元素写入顺序和excel标题顺序相同，否则标题和内容不对应
            data_list.append(sample.find(u"java.net.URL").text)
            data_list.append(sample.find(u"queryString").text)
            data_list.append(sample.get(u"lb").decode("utf-8"))
            data_list.append(sample.get(u"t"))
            data_list.append(self.convert_timestamp(sample.get(u"ts")))
            # 判断该用例是否执行成功
            is_failure = sample.find(u"assertionResult").find(u"failure").text
            if is_failure == "true":
                data_list.append("fail")
            else:
                data_list.append("pass")

            data_list.append(sample.get(u"rc"))
            data_list.append(sample.get(u"rm"))
            # 执行成功的用例在xml文件中没有failureMessage标签，需要手动写入空字符串
            if is_failure == "true":
                data_list.append(sample.find(u"assertionResult").find(u"failureMessage").text)
            else:
                data_list.append("")
            response_data = sample.find(u"responseData").text
            if not response_data: response_data = ""
            if len(response_data) > 2000:
                # 只保存2000个response字符
                data_list.append(response_data[:1999])
            else:
                data_list.append(response_data)
            print u"提取数据到:%s" % data_list
            result_list.append(data_list)
        print u"数据提取完成"

        return result_list


class ParseConfig(object):
    """
    该类主要从cfg配置文件中读取各种所需数据
    """

    def __init__(self, cfg_file_path="config.cfg"):
        self.conf = ConfigParser.ConfigParser()
        try:
            self.conf.read(cfg_file_path)
        except IOError, e:
            print u"请检查%s配置文件是否存在..." % cfg_file_path
            print e
            exit(0)

    def get_email_server(self):
        """
        从配置文件中获取获取邮箱服务器
        :return:
        """
        return self.conf.get("info", "server")

    def get_server_port(self):
        """
        获取端口
        :return:
        """
        return int(self.conf.get("info", "port"))

    def get_email_from(self):
        """
        从配置文件中获取发件人邮箱地址
        :return:
        """
        return self.conf.get("info", "from")

    def get_pwd(self):
        """
        从配置文件中获取登录密码
        :return:
        """
        return self.conf.get("info", "pwd")

    def get_email_to(self):
        """
        从配置文件中获取收件人地址
        :return: 返回收件人列表
        """
        return self.conf.get("info", "to")

    def get_email_cc(self):
        """
        从配置文件中获取抄送地址
        :return: 返回抄送列表
        """
        return self.conf.get("info", "cc")

    def get_result_xml_path(self):
        """
        获取jmeter生成的xml结果文件完整路径
        :return:
        """
        return self.conf.get("info", "result_xml_path")

    def get_send_excel_type(self):
        """
        获取需要发送excel文件种类：所有结果的还是只有失败的
        :return:
        """
        return self.conf.get("info", "only_failure")

    def get_test_plan_name(self):
        """
        获取测试项目名称
        :return:
        """
        return self.conf.get("info", "test_plan_name").decode("utf-8")

    def get_question_contact(self):
        question_contact = self.conf.get("info", "question_contact").split(",")
        contact_str = ""
        for i in range(len(question_contact)):
            if i != len(question_contact) - 1:
                temp = question_contact[i] + u" | "
            else:
                temp = question_contact[i]

            contact_str = contact_str + temp

        return contact_str


def get_email_content(test_plan_name, start_time, end_time, fail_result, result_total, fail_total, question_contact):
    """
    生成邮件内容
    :param test_plan_name:测试项目名称
    :param start_time:测试开始时间
    :param end_time:测试结束时间
    :param fail_result: 执行失败的结果信息列表
    :param result_total: 执行用例总数
    :param fail_total: 失败用例总数
    :param question_contact: 问题联系人
    :return: 邮件内容
    """
    pass_total = result_total - fail_total
    pass_percent = "%d%%" % int(round(float(pass_total) / float(result_total), 2) * 100)
    html_head = """
    <html ><head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Untitled Document</title>
    </head>

    <body>
    <table cellspacing="0" cellpadding="4" border="1" align="center">
    <thead>
    <tr bgcolor="#F3F3F3"> <td style="text-align:center" colspan="4"><b>%s接口自动化测试报告SUMMARY</b></td> </tr>

    <tr bgcolor="#F3F3F3">
    <td colspan="2" align="center"><b>开始时间</b></td>
    <td colspan="2" align="center"><b>结束时间</b></td>
    </tr>
    <tr>
    <td colspan="2" align="center">%s</td>
    <td colspan="2" align="center">%s</td>
    </tr>

    <tr bgcolor="#F3F3F3">
    <td style="width:400px" align="center"><b>用例总数</b></td>
    <td style="width:150px" align="center"><b>通过</b></td>
    <td style="width:150px" align="center"><b>不通过</b></td>
    <td style="width:300px" align="center"><b>通过率</b></td>
    </tr>

    <tr>
    <td align="center">%d</td>
    <td align="center"><b><span style="color:#66CC00">%d</span></b></td>
    <td align="center"><b><span style="color:#FF3333">%d</span></b></td>
    <td align="center">%s</td>
    </tr>

    <tr bgcolor="#F3F3F3">
    <td colspan="4" align="center"><b>用例执行失败信息</b></td>
    </tr>
    <tr>
    <td align="center"><b>接口URL</b></td>
    <td align="center"><b>执行时间</b></td>
    <td align="center"><b>response code</b></td>
    <td align="center"><b>失败信息</b></td>
    </tr>
    """ % (test_plan_name, start_time, end_time, result_total, pass_total, fail_total, pass_percent)

    fail_str = ""
    for data in fail_result:
        temp_str = """<tr>
        <td>%s</td>
        <td align="center">%s</td>
        <td align="center">%s</td>
        <td>%s</td>
        </tr>
        """ % (data[0], data[4], data[6], data[8])
        fail_str = fail_str + temp_str

    button_str = """</table><br><p>
    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;执行用例结果详细信息请查看附件文件。</b><br>
    <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;该邮件为系统自动发送,请勿回复。</b><br><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>如有疑问请联系:&nbsp;</b>%s</p>
    </body></html>""" % question_contact
    html_content = html_head + fail_str + button_str

    return html_content


def send_mail(content, attachs):
    """
    发送测试报告邮件
    :param content: 邮件内容
    :param attachs: 附件路径，类型为list
    :return:
    """
    # 从配置文件中获取邮箱配置信息
    pcfg = ParseConfig()
    email_from = pcfg.get_email_from()
    email_server = pcfg.get_email_server()
    port = pcfg.get_server_port()
    login_pwd = pcfg.get_pwd()
    email_to = pcfg.get_email_to()
    email_cc = pcfg.get_email_cc()
    project_name = pcfg.get_test_plan_name()

    msg = MIMEMultipart("related")
    msg["Subject"] = project_name + u"接口自动化测试报告_" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    # To和Cc中有多个邮箱地址时不能是列表，应该为字符创且每个邮箱用逗号隔开
    msg["To"] = email_to
    if email_cc != "":
        msg["Cc"] = email_cc
    msg["From"] = email_from

    if email_to == "":
        print u"收件人为空，请检查配置文件是否正确..."
        exit(0)

    msg_text = MIMEText(content, _subtype="html", _charset="utf-8")
    msg.attach(msg_text)

    # 添加附件
    for attach_file in attachs:
        attach = MIMEText(open(attach_file, "rb").read(), "base64", "utf-8")
        attach["Content-Type"] = "application/octet-stream"
        attach["Content-Disposition"] = "attachment; filename=" + os.path.split(attach_file)[1]
        msg.attach(attach)

    try:
        server = smtplib.SMTP_SSL(email_server, port, timeout=30)
        print u"正在登录邮箱服务器%s,端口号:%d" % (email_server, int(port))
        server.login(email_from, login_pwd)
        print u"登录邮箱服务器成功"
        print u"邮件收件人:%s" % str(email_to)
        print u"邮件抄送人:%s" % str(email_cc)
        print u"邮件发送中..."
        # sendmail方法中收邮件的地址必须为列表，如果有抄送人时，抄送人和收件人合并到一个列表中
        # mailbox_list = []
        if email_cc == "":
            mailbox_list = email_to.split(",")
        else:
            mailbox_list = email_to.split(",") + email_cc.split(",")
        server.sendmail(email_from, mailbox_list, msg.as_string())
        server.quit()
        print u"邮件发送成功"
    except Exception, e:
        print u"发送邮件失败"
        print e


def main():
    rd = ResultData()
    rd.write_excel("all")
    if rd.get_failure_result_num() != 0: rd.write_excel("failure")
    rd.backup_result_xml(rd.get_result_xml_path())
    if rd.get_failure_result_num() == 0:
        print u"所有用例全部通过，不发送邮件"
        exit(0)

    pcfg = ParseConfig()
    only_fail = pcfg.get_send_excel_type()
    attach_file = []
    if only_fail == "true":
        attach_file.append(rd.excel_path_fail)
    else:
        attach_file.append(rd.excel_path_all)

    mail_content = get_email_content(rd.get_test_plan_name(), rd.get_start_time(), rd.get_end_time(),
                                     rd.get_failure_result(), rd.get_all_result_num(), rd.get_failure_result_num(),
                                     pcfg.get_question_contact())
    send_mail(mail_content, attach_file)


if __name__ == "__main__":
    main()
