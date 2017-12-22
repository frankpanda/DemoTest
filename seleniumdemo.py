#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import time
from selenium import webdriver

__author__ = "frank xiong"


def test_baidu_firefox():
    driver = webdriver.Firefox()

    driver.get("http://www.baidu.com")
    time.sleep(3)
    search_fild = driver.find_element_by_name("wd")
    print u"测试1..."
    search_fild.send_keys(u"奥运会")
    print u"测试2..."
    time.sleep(3)
    search_button = driver.find_element_by_id("su")
    search_button.click()

    print "ok!"


if __name__ == "__main__":
    test_baidu_firefox()
