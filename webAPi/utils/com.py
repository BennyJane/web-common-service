# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

import datetime
import hashlib
import os
import time


def produce_id():
    path = os.getcwd()
    src = path + str(time.time())
    m = hashlib.md5()
    m.update(src.encode('utf-8'))
    return m.hexdigest()


def setSHA256(passWord):
    # 加密密码 ssh56
    hhb = hashlib.sha256()
    # 有返回值, 但没有必要添加
    hhb.update(bytes(passWord, encoding='utf-8'))
    return hhb.hexdigest()


def getFormatDate(date=None, _format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(_format)




