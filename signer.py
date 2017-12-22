#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time

__author__ = "frank xiong"


def get_sign():
    params = {
        "app_key": "123",
        "method": "test_method",
        "operator": "熊兵",
        "user_id": 1000,
        "channel": "mode",
        "content": "测试test",
        "mobile": "16776786",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "city": "GZ"
    }

    temp_string = ["123"]
    for key in sorted(params.keys()):
        if not isinstance(params[key], str):
            print key, params[key]
            temp_string.append(key + str(params[key]))
        else:
            temp_string.append(key + params[key])

    temp_string.append("123")
    param_string = "".join(temp_string)
    print param_string


if __name__ == "__main__":
    get_sign()
