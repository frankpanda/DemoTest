#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import xml.dom.minidom as Dom

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

__author__ = 'Huoyunren'

file_path = r"config\demo.xml"


def write_xml_by_dom():
    """
    用dom来写一个xml
    :return:
    """
    xml_doc = Dom.Document()
    # 创建根节点
    root_node = xml_doc.createElement("info")
    # 添加属性和值
    root_node.setAttribute("dicrip", u"测试Text")
    # 把根节点添加到xml文档
    xml_doc.appendChild(root_node)

    book_node = xml_doc.createElement("book")
    book_node.setAttribute("is_borrow", "False")
    root_node.appendChild(book_node)

    name_node = xml_doc.createElement("name")
    # 创建节点的标签值
    name_node_value = xml_doc.createTextNode(u"人性的弱点")
    # 把节点标签值添加到指定节点
    name_node.appendChild(name_node_value)
    book_node.appendChild(name_node)

    # 创建price标签
    price_node = xml_doc.createElement("price")
    price_node_value = xml_doc.createTextNode("60")
    price_node.appendChild(price_node_value)
    book_node.appendChild(price_node)

    # 保存xml文件
    xml_file = open(r"config/created.xml", "w")
    xml_file.write(xml_doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
    xml_file.close()


def write_xml_by_et():
    """
    用ET来写xml文件
    :return:
    """
    try:
        tree = ET.parse(file_path)
    except Exception, e:
        print u"读取xml文件异常："
        print e
    root = tree.getroot()
    for name in root.iter("name"):
        if name.attrib["attr"] == "frank":
            print u"已找到frank，正在执行操作..."
            # 添加修改属性
            name.set("attr", "frank_xiong")
            name.set("is_fishing", "true")

            # 修改文本
            name.find("age").text = "18"

            # 添加孩子
            car = ET.Element("car")
            car.text = u"标致308"
            name.append(car)
        else:
            print u"抱歉，没有找到frank..."
        break
    tree.write(file_path, encoding="utf-8", xml_declaration=True)


def read_xml_by_dom():
    """
    用dom来读取xml文件，dom适合读取小型的xml文件
    因为dom是一次性把整个xml文件读取到内存里面
    :return:
    """
    # 打开xml文档
    dom = Dom.parse(file_path)
    # 获取文档元素对象
    data = dom.documentElement
    name_tag = data.getElementsByTagName("name")
    for info in name_tag:
        print "*************info**************"
        print "id:", info.getAttribute("id")
        print "name:", info.getAttribute("attr")
        sex = info.getElementsByTagName("sex")[0]
        print "sex:", sex.childNodes[0].data
        age = info.getElementsByTagName("age")[0]
        print "age:", age.childNodes[0].data
        courses = info.getElementsByTagName("courses")[0]
        math = courses.getElementsByTagName("math")[0]
        print "math:", math.childNodes[0].data
        en = courses.getElementsByTagName("en")[0]
        print "English:", en.childNodes[0].data


def read_xml_by_et():
    """
    用ET来读取xml文件
    :return:
    """
    try:
        # 打开xml文件
        tree = ET.parse(file_path)
        # 从字符串读取xml
        # tree = ET.fromstring(xml_string)
        # 获取root节点
        root = tree.getroot()
        print root
    except Exception, e:
        print u"读取xml文件异常..."
        print e
    print root.tag, "---", root.attrib
    file_write = open(u"D:/test.txt", "w")
    for child in root:
        print child.tag, "--->", child.attrib
        if child.attrib:
            print type(child.attrib["attr"])
            print u"姓名：", child.attrib["attr"].encode("utf-8")
            file_write.write(child.attrib["attr"].encode("utf-8") + "\n")
    file_write.close()

    # 访问child by索引
    print "time -->", root[1][1].text

    # 通过迭代来访问特定的元素
    for temp in root.iter("name"):
        name_attr = temp.attrib["attr"]
        print name_attr.encode("utf-8") + ":"
        elem_math = temp.find("courses").find("math")
        math_grade = elem_math.text
        print "math grade:" + math_grade

    for grade in root.iter("math"):
        print u"math的分数为：%s" % grade.text


if __name__ == '__main__':
    # read_xml_by_dom(file_path)
    read_xml_by_et()
    # write_xml_by_et()
    # write_xml_by_dom()
