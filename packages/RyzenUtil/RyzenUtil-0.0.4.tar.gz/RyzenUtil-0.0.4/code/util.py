# -*- coding: utf-8 -*-
# @Time : 2020/11/19 下午4:01
# @File : util.py

import time
from functools import wraps

import requests


def static_request_time(func):
    """
    统计func运行的时长
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        t = end_time - start_time
        print(f"time: {t} \n")
        return res

    return decorated


def retry(func):
    """
    对func进行重试，次数：3
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        res = ""
        for _ in range(3):
            try:
                res = func(*args, **kwargs)
                if _ > 0:
                    print(f"{get_time()} retry {_}")
                break
            except BaseException as e:
                print(e.args)
        return res

    return decorated


def get_time():
    """
    获取当前的时间字符串
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


@retry
def get_data_from_url(url):
    """
    网络请求（自动重试3次）

    :argument
        url: 请求地质
    """
    return requests.get(url, timeout=30).text
