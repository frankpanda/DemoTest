# -*- coding: utf_8 -*-
import json
import time
import httplib
import csv

# hsotname = "api.pre.sxw.cn"
host_gateway = "116.62.26.185:8100"
host_sxt = "120.26.244.205:8092"
# 登录
stu_login_url = r"/uic/api/auth/login/cipher"
parents_login_url = r'/uic/api/auth/mobile_login/cipher'
# 个人信息
findcuser = '/platform/api/account/find_current_user'
# 考试分数
getclassidurl = "/analysis/api/mobile/student/find_score_list"
# 考试列表
page_stu_uri = "/exam/api/query/page_for_student"
# 真题查询
query_question_uri = "/sxtnew/mobile/questionController/queryRealQuestion.do"

# 相关文件路径
userpath = "stu_account.txt"
tokenpath = "e:/test_data.txt"

header = {"Content-Type": "application/json",
          "ACCEPT": "*/*",
          "Connection": "close",
          "charset": "UTF-8"}

# login password
pwd = 'Ze48Lq7/iiHPtyAtsopZfw=='


def cleanfile():
    fileo = open(tokenpath, "w")
    fileo.write("")
    fileo.close()


fw = open(tokenpath, "a+")


def writetoken(value):
    # fileo = open(tokenpath ,"a+")
    fw.write(value + "\n")


def closef():
    fw.close()


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


# 新建token文件
cleanfile()
countor = 0

for line in open(userpath, "r"):
    print "writting %s" % line

    """
    *******************************************链接gateway服务器********************************************
    """
    conn_gateway = httplib.HTTPConnection(host_gateway)
    conn_gateway.timeout = 3
    try:
        """
        # 家长端登录提交数据
        body = {
            "password": "Ze48Lq7/iiHPtyAtsopZfw==", "clientId": "6da0e296d85d68eed566bcd224cde1e2",
            "appVersion": "1.5.9", "appType": "sxt-android-parents", "imei": "000000000000000",
            "userType": "3",
            "client": "1", "appVersionCode": "62", "account": str(line.strip()),
            "macAddr": "000000000000000",
            "loginIdentityType": ""
        }
        
        """

        # 学生端登录提交数据
        body = {
            'userType': 1,
            'client': 2,
            'account': line.strip(),
            'password': pwd,
            'clientIdentity': ''
        }
        value = json.dumps(body)

        # 登录
        conn_gateway.request('POST', url=stu_login_url, body=value, headers=header)
        content = conn_gateway.getresponse().read()
        # print content

        returnvalue = content.replace('true', "True").replace("false", "False")
        t = eval(returnvalue)
        tokenvalue = t['data']['token']
        # userid = t["data"]["accountLoginResponse"]["accountId"]

        #  writetoken(line.strip() + "==" + tokenvalue)
    except Exception, e:
        print line.strip() + " login error"
        print "----------------------------------"
        print e
        continue

    header1 = {"Content-Type": "application/json",
               "ACCEPT": "*/*",
               "charset": "UTF-8",
               "Connection": "close",
               "token": tokenvalue
               }
    '''
    
    try:
        conn_gateway.request('GET', url=findcuser, headers=header1)

        content = conn_gateway.getresponse().read()

        t = content.replace("true", "True").replace("false", "False")

        infor = eval(t)
        # get student account id
        studendsid = infor['data']['id']
        # schoolid = infor["data"]["orgid"]
        # tenatid = infor["data"]["tenantid"]
    except Exception, e:
        print findcuser
        print e
        studendsid = 0
        # schoolid = 0
        # tenatid = 0
    '''
    conn_gateway.close()

    # writetoken(tokenvalue)
    # 加这个等待时间，可以把时间调大点，防止报错。。以秒为单位
    # 错误 requests.exceptions.ConnectionError: HTTPConnectionPool(host='api.pre.sxw.cn', port=80): Max retries exceeded with url:
    # 参考 http://blog.csdn.net/huaweitman/article/details/9617453
    # time.sleep(0.05)

    # 注释开始--------------------------------

    """
    ********************************************链接sxt服务器**************************************
    """

    conn_sxt = httplib.HTTPConnection(host_sxt)
    conn_sxt.timeout = 3

    try:
        conn_sxt.request("POST", url="/sxtnew/mobile/xbController/getTheLatestExam.do", headers=header1)
        content = conn_sxt.getresponse().read()
        t = content.replace("true", "True").replace("false", "False")
        infor = eval(t)

        exid = infor["attributes"]["exam"]["id"]

    except Exception, e:
        print e
        continue

    try:
        conn_sxt.request("POST", url="/sxtnew/mobile/xbController/getOneExamAllSubjectSpeaks.do?examId=" + str(exid),
                         headers=header1)
        content = conn_sxt.getresponse().read()
        t = content.replace("true", "True").replace("false", "False")
        infor = eval(t)

        xbsexid = infor["attributes"]["subjects"][0]["subjectId"]

    except Exception, e:
        print e
        continue

    if tokenvalue != "":
        writeline = str(exid) + "," + str(xbsexid) + "," + tokenvalue
        writetoken(writeline)
        countor += 1
        print countor

    """
    try:
        conn.request('POST', url=query_question_uri + "?exam_type=-1&pageNumber=1&type=1&pageSize=20", headers=header1)
        content = conn.getresponse().read()
        t = content.replace("true", "True").replace("false", "False")
        infor = eval(t)

        examid_a = infor["attributes"]["exams"][0]["exam_id"]
        courseid_a = infor["attributes"]["exams"][0]["courses"][0]["id"]

    except Exception, e:
        print examid_a, courseid_a
        print e
        continue

    try:
        conn.request('POST',
                     url="/sxtnew/mobile/questionController/queryOneCourseRealQuestions.do?exam_id=" + examid_a + "&courseid=" + courseid_a + "&pageNumber=1&pageSize=10&examType=0",
                     headers=header1)
        content = conn.getresponse().read()
        t = content.replace("true", "True").replace("false", "False")
        infor = eval(t)

        questionid = infor["attributes"]["questions"][0]["id"]
        # print questionid
    except Exception, e:
        print e
        continue

    # 写入信息：
    if tokenvalue != "":
        writeline = str(studendsid) + "," + str(questionid) + "," + tokenvalue
        writetoken(writeline)
        countor += 1
        print countor
    """

    """

    try:
        body = {"pageableDto": {"page": 1, "size": 10}, "studentAccountId": studendsid}
        conn.request('POST', url=page_stu_uri, headers=header1, body=json.dumps(body))
        content = conn.getresponse().read()
        t = content.replace("true", "True").replace("false", "False")
        infor = eval(t)

        examid = infor['data']['dataList'][0]['id']
    except Exception, e:
        print page_stu_uri
        print e
        examid = 0

    try:
        body = {"examId": examid, "accountId": studendsid}
        conn.request('GET', url=getclassidurl + "?examId=" + str(examid) + "&accountId=" + str(studendsid),
                     headers=header1)
        content = conn.getresponse().read()
        t = content.replace("true", "True").replace("false", "False")
        infor = eval(t)

        classid = infor['data'][0]['classId']
        examCourseId = infor['data'][1]['examCourseId']
    except Exception, e:
        print getclassidurl
        print e
        classid = 0

    # 写入信息：学生ID,身份证，token
    if tokenvalue != "" and studendsid != 0:
        writeline = str(studendsid) + "," + line.strip() + "," + tokenvalue + "," + str(schoolid) + "," + str(
            tenatid) + "," + str(examid) + "," + str(classid) + ',' + str(examCourseId)
        writetoken(writeline)
        countor += 1
        print countor
     """

    # ====================================================================
    '''
    # 获取studen 的 classid
    header1 = {"Content-Type": "application/json",
              "ACCEPT": "*/*",
              "charset":"UTF-8",
              "Connection":"close",
              "token": tokenvalue
               }
    #TODO: 固定考试ID
    datas = {"examId":"000000000000120000000182","accountId":studendsid}
    value = json.dumps(datas)
    try:
        conn.request('POST',url=getclassidurl,body=value,headers=header1)
        response = conn.getresponse().read()

        value = response.replace("true","True").replace("false","False")

        td = eval(value)

        if value.__contains__("classId"):
            classid = td["data"][0]["classId"]
            #classid = 0
            # 获取学生的 班级ID,学生ID,身份证，token，最后写入txt文件
            if tokenvalue!="":
                writeline = str(classid) +"==" + str(studendsid) + "==" + line.strip() + "==" + tokenvalue
                writetoken(writeline)
        else:
            print  line.strip() + " -- 未参加该考试"
    except:
        pass


    # 注释结束  --------------------------------
    '''
    conn_sxt.close()
# 最后关闭文件对象
closef()
