# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import base64
import io
import os
import string
import time
import json
import random
import hashlib
import datetime

import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

from webAPi.log import web_logger
from config import projectConfigs
from webAPi.constant import ReqJson


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


def cron_params(data):
    params = {
        "job_id": data[0],
        "cron": json.loads(data[1]),
        "callback_url": data[2],
        "loop": data[3]
    }
    return params


def get_config_from_env(config_name=None):
    """根据环境变量获取当前配置信息"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in projectConfigs.keys():
            config_name = 'development'
    return projectConfigs[config_name]


"""
===================================================================================
重写flask-restful的异常处理函数，修改返回json格式
前期替代方案： 使用flask钩子 after_request(response)函数，捕捉status_code != 200的请求
因为这些请求被flask-restful处理，返回json格式数据，但是状态码不为200
===================================================================================
"""


def error_router(self, original_handler, e):
    """This function decides whether the error occured in a flask-restful
    endpoint or not. If it happened in a flask-restful endpoint, our
    handler will be dispatched. If it happened in an unrelated view, the
    app's original error handler will be dispatched.
    In the event that the error occurred in a flask-restful endpoint but
    the local handler can't resolve the situation, the router will fall
    back onto the original_handler as last resort.

    :param original_handler: the original Flask error handler for the app
    :type original_handler: function
    :param e: the exception raised while handling the request
    :type e: Exception

    """
    if self._has_fr_route():
        try:

            return get_error_message_by_flask_restful(self.handle_error(e))
        except Exception:
            pass  # Fall through to original handler
    return original_handler(e)


def get_error_message_by_flask_restful(res):
    req = ReqJson()
    res = json.loads(res.data)
    print("res", res)
    msg = res.get("message", "")
    if isinstance(msg, dict):
        req.msg = '; '.join([i for i in msg.values()])
    elif isinstance(msg, str):
        req.msg = msg
    return req.result


"""
===================================================================================
图形验证码
===================================================================================
"""


class CaptchaTool(object):
    def __init__(self, width=50, height=12):
        self.width = width
        self.height = height
        self.img = Image.new("RGB", (width, height), 'white')  # 新图片
        self.font = ImageFont.load_default()  # 字体
        self.draw = ImageDraw.Draw(self.img)  # draw对象，绘制线条

    def draw_line(self, num=3):
        for num in range(num):
            x1 = random.randint(0, self.width / 2)
            y1 = random.randint(0, self.height / 2)
            x2 = random.randint(0, self.width)
            y2 = random.randint(self.height / 2, self.height)
            self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def get_verify_code(self, width, height):
        code = ''.join(random.sample(string.digits, 4))  # 随机生成四个字符
        for item in range(4):
            self.draw.text(
                (6 + random.randint(-3, 3) + 10 * item, 2 + random.randint(-2, 2)),  # 子位置
                text=code[item],  # 单个字符
                fill=(random.randint(32, 127),  # 生成随机色彩
                      random.randint(32, 127),
                      random.randint(32, 127)
                      ),
                font=self.font
            )
        # self.draw_line()  # 绘制干扰线
        # self.img = self.img.filter(ImageFilter.GaussianBlur(radius=0.2))  # 绘制高斯干扰线条
        self.img = self.img.resize((width, height))  # 重新设置大小
        buffered = io.BytesIO()
        self.img.save(buffered, format="JPEG")
        img_str = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
        return img_str.decode('utf-8'), code
