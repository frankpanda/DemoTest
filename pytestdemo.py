#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pytest
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = "frank xiong"


def demo_plus(n):
    result = n + 1
    return result


def test_ok_1():
    """
    成功
    :return:
    """
    assert demo_plus(3) == 4


def test_faild_1():
    """
    失败
    :return:
    """
    assert demo_plus(3) == 5


def test_faild_2():
    assert demo_plus(6) == 8
    print "失败！"


def test_ok_2():
    assert demo_plus(6) == 7
    print "成功！"


if __name__ == "__main__":
    pytest.main("--maxfail=2 -s pytestdemo.py")
