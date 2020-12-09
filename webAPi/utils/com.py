# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

import os
import time
import hashlib
import datetime
import requests
from webAPi.log import web_logger


def produce_id():
    path = os.getcwd()
    src = path + str(time.time())
    m = hashlib.md5()
    m.update(src.encode('utf-8'))
    return m.hexdigest()


def setSHA256(password):
    # 加密密码 ssh56
    hhb = hashlib.sha256()
    # 有返回值, 但没有必要添加
    hhb.update(bytes(password, encoding='utf-8'))
    return hhb.hexdigest()


def getFormatDate(date=None, _format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(_format)


def request_send_mail(params, domain=None):
    url = f"{domain}/api/v1/mail/task/execute"
    headers = {'Content-Type': 'application/json'}  # 发送json数据
    res = requests.post(url, data=params, headers=headers)
    # TODO 添加邮件发送结果的记录功能
    if res.status_code != 200:
        # 添加日志，记录邮件发送失败的情况
        web_logger.debug(f"【邮件发送失败】：状态码：{res.status_code}，错误信息： {res.text} ")

    else:
        web_logger.info("邮件发送成功！")


def cron_date(params):
    year = params.get("year")
    month = params.get("month")
    day = params.get("day")
    hour = params.get("hour")
    minute = params.get("minute")
    second = params.get("second")
    try:
        target_date = datetime.datetime(year, month, day, hour, minute, second)
    except Exception as e:
        raise Exception("日期格式不正确")
    return target_date
