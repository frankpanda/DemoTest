#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
from email.utils import formatdate
from xlwt import *
import xlwt
import os
from xlutils.copy import copy
import sys
import xlrd
import xml.dom.minidom

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding("utf-8")

testhistory = sys.path[0] + "/resulthistory/"


class resltanslsys:
    def __init__(self):
        """
        初始化各时间戳
        """
        self.current_time = self.getcurrentdate()
        self.currnet_date = self.getcurrentdate()
        self.current_date_hour = self.getdatehour()
        self.case_total_num = 0
        self.case_pass_num = 0
        self.case_failure_num = 0

    def getcurrenttime(self):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    def getcurrentdate(self):
        return time.strftime('%Y%m%d', time.localtime(time.time()))

    def getdatehour(self):
        return time.strftime('%Y%m%d%H', time.localtime(time.time()))

    def writeExcel(self, filepath, resultlist=[]):
        """
        create new excel file
        """
        if os.path.isfile(filepath): os.remove(filepath)
        if not os.path.isfile(filepath):
            w = Workbook()
            w.add_sheet('result')
            ws = w.get_sheet(0)
            # title
            array = [u"接口URL", u"耗时（毫秒）", u"执行时间",
                     u"成功否", u"返回状态码", u"返回信息", u"错误信息"]
            col = 0
            for v in array:
                ws.write(0, col, v)
                col += 1
            w.save(filepath)

        # detail message
        rb = xlrd.open_workbook(filepath)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        rownumber = 1
        for row in resultlist:
            col = 0
            array = []
            array.append(str(row['label']).decode('utf-8'))
            array.append(row['elapsed'])
            array.append(row['timeStamp'])
            array.append(row['success'])
            array.append(row['responseCode'])
            array.append(row['responseMessage'])
            array.append(str(row['failureMessage']).decode('utf-8'))
            for v in array:
                ws.write(rownumber, col, v)
                col += 1
            rownumber += 1
        wb.save(filepath)

    def write_excel(self, save_type="failure"):
        '''
        从测试结果的xml文件中提取所需数据并保存到excel文件中
        :param save_type: 保存成功、失败或者所有数据到excel文件(pass:成功，failure:失败,all:所有)
        :return:
        '''

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(u"result")
        # 列名
        head_list = [u"接口URL", u'参数', u"用例名", u"耗时(毫秒)", u"执行时间", u"测试结果", u"响应码", u"响应信息", u"断言错误信息", u"响应数据"]
        # 写入标题
        for i in range(len(head_list)):
            worksheet.write(0, i, head_list[i])

        data_list = self.get_result_data_from_xml()
        row_num = 1
        print u"开始把数据写入Excel文件中..."
        for data in data_list:
            if save_type == "failure":
                if data[5] == "fail":
                    self.case_failure_num += 1
                    # print u"正在写入第%d条数据..." % self.case_failure_num
                    for i in range(len(data)):
                        worksheet.write(self.case_failure_num, i, data[i])

            elif save_type == "pass":
                if data[5] == "pass":
                    self.case_pass_num += 1
                    # print u"正在写入第%d条数据..." % self.case_pass_num
                    for i in range(len(data)):
                        worksheet.write(self.case_pass_num, i, data[i])

            elif save_type == "all":
                self.case_total_num += 1
                # print u"正在写入第%d条数据..." % self.case_total_num
                for i in range(len(data)):
                    worksheet.write(self.case_total_num, i, data[i])

        if save_type == "pass":
            excel_path = self.creatfilename(u"TestResult_Pass")
            workbook.save(excel_path)
        elif save_type == "failure":
            excel_path = self.creatfilename(u"TestResult_Failure")
            workbook.save(excel_path)
        else:
            excel_path = self.creatfilename(u"TestResult_All")
            workbook.save(excel_path + "TestResult_All.xls")
        print u"生成%s文件成功" % os.path.split(excel_path)[1]

    def get_result_data_from_xml(self):
        '''
        从jmeter生成的xml文件中提取需要的关键字信息
        :return: 返回获取到的数据作为列表返回
        '''
        # 获取jmeter生成的xml文件路径
        cx = CreatXml("mailconfig.xml")
        result_xml_path = cx.getjtlpath() + u"result.xml"

        xml_data = ET.parse(result_xml_path)
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
            data_list.append(self.convertimstamptodatetime(sample.get(u"ts")))
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
            data_list.append(sample.find(u"responseData").text)
            print data_list
            result_list.append(data_list)
            print u"数据提取完成"

        return result_list

    def send_email(self, mailhost, mailport, username, passwd, send_to, subject, content, files=[]):
        msg = MIMEMultipart()
        for f in files:
            att = MIMEBase('application', 'octet-stream')
            att = MIMEText(open(f, 'rb').read(), 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            attachname = os.path.basename(f)
            att["Content-Disposition"] = 'attachment; filename=%s' % attachname.encode("utf8")
            msg.attach(att)

        msg['From'] = username
        msg['Subject'] = u'%s' % subject
        msg['To'] = ",".join(send_to)
        msg['Date'] = formatdate(localtime=True)

        body = MIMEText(content.encode('utf8'), _subtype='html', _charset='utf8')
        msg.attach(body)

        try:
            s = smtplib.SMTP_SSL(mailhost, int(mailport), timeout=20)
        except:
            print " ERROR:Connect to mail server(%s):port(%s) timeout" % (mailhost, mailport)
            print "----------------------------------------------"
            return False

        try:
            s.login(username, passwd)
        except:
            # 送邮件失败，请确认发件人的邮箱地址和密码是否正确
            print " ERROR:Send email failed, Please check the account or password is right."
            print "----------------------------------------------"
            s.close()
            return False

        try:
            s.sendmail(username, send_to, msg.as_string())
            s.close()
            return True
        except:
            # 发送邮件失败，确认邮箱是否能正确访问
            print " ERROR:Send email failed,Please check Whether the server is properly accessible." + '\n'
            print "----------------------------------------------"
            s.close
            return False

    def convertimstamptodatetime(self, timestamp):
        timeStamp = str(timestamp)[0:-3]
        timeArray = time.localtime(long(timeStamp))
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    # timeStamp, elapsed, label,responseCode, responseMessage,
    # threadName, dataType,success,failureMessage,bytes,grpThreads,
    # allThreads,Latency,IdleTime
    def analysisjtlfile(self, jtlfolder, filelist):
        wholefailedresult = []
        wholeresult = []

        for f in filelist:
            if not jtlfolder.endswith("/"):
                jtlpath = jtlfolder + "/" + f
            else:
                jtlpath = jtlfolder + f
                print "Start to analysis jtl file : " + jtlpath

                with open(jtlpath) as fo:
                    for line in fo:
                        singlerow = {}
                        if line.startswith("timeStamp"):
                            continue
                        result = line.split(",")
                        singlerow["timeStamp"] = self.convertimstamptodatetime(result[0])
                        singlerow["elapsed"] = result[1]
                        singlerow["label"] = result[2]
                        singlerow["responseCode"] = result[3]
                        singlerow["responseMessage"] = result[4]
                        singlerow["success"] = result[7]
                        singlerow["failureMessage"] = result[8]
                        wholeresult.append(singlerow)
                        if result[7].lower().strip() == "false":
                            wholefailedresult.append(singlerow)
                print "Analysis jtl file[ %s ] success .........." % (jtlpath)

        return wholeresult, wholefailedresult

    def getmailcontent(self, wholeresult, wholefailedresult):
        content = u"""<html xmlns="http://www.w3.org/1999/xhtml">
                    <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
                    <body>
                       <H3>您好！<H3>
                        &nbsp;附件是本次接口测试的测试结果，请查收！<br><br> """
        content += u"""&nbsp;本次测试共执行 """ + \
                   str(len(wholeresult)) + u""" 个接口，其中失败  <font color="#FF0000">""" + \
                   str(len(wholefailedresult)) + u"""</font>  个,失败的接口如下(只显示前10条记录）：<br>"""
        displaycount = len(wholefailedresult)
        if displaycount > 10: displaycount = 10
        for i in range(displaycount):
            x = wholefailedresult[i]

            responsecode = str(x["responseCode"]).decode("utf-8")
            url = str(x["label"]).decode("utf-8")
            content += u"&nbsp;&nbsp;接口URL: " + url + u" |&nbsp;返回code: " + responsecode

            responsemessage = str(x["responseMessage"]).decode("utf-8")
            failmessage = str(x["failureMessage"].replace('"', '')).decode("utf-8")
            content += u" |&nbsp;返回信息: " + responsemessage + u" |&nbsp;失败信息: " + failmessage + "<br>"

        content += u""" <br> 谢谢<br>"""
        content += u"发送时间：" + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) \
                   + u""" <br><p><font color="#FF1CAE">注：这是一封自动发送的邮件,请不要回复。</font></p>
                    &nbsp;&nbsp;&nbsp;&nbsp;附件是测试失败的接口列表<br>
                  </font>  </p>
              </body>
            </html> """
        return content

    def creatfilename(self, flag_name):
        '''
        按照日期每天创建存放excel文件的文件夹，并生成excel文件名
        :param flag_name: excel文件名标签如pass，failure，all等等
        :return: excel路径
        '''
        log_path = self.currnet_date + u"/"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        excel_path = log_path + flag_name + "_" + self.current_time + ".xls"
        return excel_path


class CreatXml:
    def __init__(self, mailxmlfile):
        self.dom = xml.dom.minidom.parse(mailxmlfile)
        self.root = self.dom.documentElement

    def get_nodevalue(self, node, index=0):
        return node.childNodes[index].nodeValue

    def get_xmlnode(self, name):
        return self.root.getElementsByTagName(name)

    def getsendtolist(self):
        unode = self.root.getElementsByTagName("recivelist")
        nodevalue = unode[0].childNodes[0].nodeValue
        return str(nodevalue).strip()

    def getmailport(self):
        unode = self.root.getElementsByTagName("mailport")
        nodevalue = unode[0].childNodes[0].nodeValue
        return str(nodevalue).strip()

    def getjtlpath(self):
        unode = self.root.getElementsByTagName("jtlpath")
        nodevalue = unode[0].childNodes[0].nodeValue
        return str(nodevalue).strip()

    def getifsend(self):
        unode = self.root.getElementsByTagName("ifsend")
        nodevalue = unode[0].childNodes[0].nodeValue
        return str(nodevalue).strip()

    def getsmptserver(self):
        try:
            unode = self.root.getElementsByTagName("mailserver")
            mailserver = unode[0].childNodes[0].nodeValue
            if str(mailserver).strip() == "":
                return "smtp.exmail.qq.com"
            else:
                return str(mailserver).strip()
        except:
            return "smtp.exmail.qq.com"

    def getfrom(self):
        try:
            unode = self.root.getElementsByTagName("whosend")
            fromwho = unode[0].childNodes[0].nodeValue
            if str(fromwho).strip() == "":
                return ""
            else:
                return str(fromwho).strip()
        except:
            return ""

    def getfrompwd(self):
        try:
            unode = self.root.getElementsByTagName("pwd")
            pwd = unode[0].childNodes[0].nodeValue
            if str(pwd).strip() == "":
                return ""
            else:
                return str(pwd).strip()
        except:
            return ""


def getjtlresultfiles(folderpath):
    """
    get Jmeter test result jtl file
    :param folderpath:
    :return:
    """
    filelist = []
    for root, dirs, files in os.walk(folderpath):
        for f in files:
            extendname = str(os.path.splitext(f)[1])
            if extendname.lower() == ".jtl":
                filelist.append(f)
    return filelist


if __name__ == "__main__":

    mailxmlfile = sys.path[0] + u"/mailconfig.xml"
    mail = CreatXml(mailxmlfile)

    print u"----------------------------------------------"
    ana = resltanslsys()
    # get result
    jtlfolder = mail.getjtlpath()
    filelist = getjtlresultfiles(jtlfolder)

    if len(filelist) > 0:

        wholeresult, wholefailedresult = ana.analysisjtlfile(jtlfolder, filelist)

        print u"----------------------------------------------"
        print "Start to create the result file........."
        wholeresultpath = ana.creatfilename("TestResult_all")
        ana.writeExcel(wholeresultpath, wholeresult)

        errorresultpath = ""
        if len(wholefailedresult) > 0:
            errorresultpath = ana.creatfilename("TestResult_failed")
            ana.writeExcel(errorresultpath, wholefailedresult)
        else:
            print "   There is no failed records.........."

        print "Create the result file end........."
        print u"----------------------------------------------"
        content = ana.getmailcontent(wholeresult, wholefailedresult)

        # [wholeresultpath,errorresultpath] is all and failed
        ifsend = mail.getifsend()
        attachfiles = []
        if ifsend.upper().__eq__("Y"):
            attachfiles.append(wholeresultpath)

        if len(errorresultpath) > 0:
            attachfiles.append(errorresultpath)

        if len(attachfiles) > 0:
            print "Start to send email..........."
            subject = ana.getdatehour() + u"_接口测试结果"
            username = mail.getfrom()
            passwd = mail.getfrompwd()
            host = mail.getsmptserver()
            sendto = mail.getsendtolist().split(",")
            mail_port = mail.getmailport()

            if not ana.send_email(host, mail_port, username, passwd, sendto, subject, content, attachfiles):
                print "Send email failed,Please check the result file manually:"
                for x in attachfiles:
                    print "    ", x
            else:
                print "Send email success........."
            print "----------------------------------------------"
        else:
            print "All interface is passed, But the config is not send email...."
            print "Please see the result file:\r\n" + wholeresultpath
            print "----------------------------------------------"
    else:
        print "WARNING: The jtl result file is not exist!"

    '''
    ana = resltanslsys()
    ana.write_excel(r"d:/result_xml/", "failure")
    '''
