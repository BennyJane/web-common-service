# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 23:34
# Warning    ：The Hard Way Is Easier
import datetime
import random
from flask_restful import Resource
from flask_restful import reqparse

from webAPi import web_logger
from webAPi.response import ReqJson
from webAPi.extensions import redis_conn
from webAPi.utils.com import getFormatDate
from webAPi.utils.phone_msg import SendSms
from webAPi.constant import REDIS_PHONE_CODE
from webAPi.constant import REDIS_PHONE_CODE_EX
from webAPi.constant import PHONE_CODE_LENGTH
from webAPi.utils.validate import validate_phone
from webAPi.constant import REDIS_PHONE_LAST_TIME
from webAPi.constant import REDIS_PHONE_TIME_GAP


class Sms(Resource):
    # 常用短信场景
    # category 参数如下：
    # authentication: 身份验证
    # login_confirmation: 登陆验证
    # login_exception: 登陆异常
    # user_registration: 用户注册
    # change_password: 修改密码
    # information_change: 信息修改
    def get(self):
        """获取手机验证码"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument("category", type=str, required=True, loction="json", help="请输入短信类型")
        parse.add_argument("phone", type=str, required=True, location="json", help="请输入手机号码")
        front_data = parse.add_argument()

        phone = front_data.get("phone")
        category = front_data.get("category")

        re_phone = validate_phone(phone)
        # 限制短信发送频率
        last_timestamp = redis_conn.hget(re_phone, REDIS_PHONE_LAST_TIME)
        if last_timestamp is not None:
            last_timestamp = getFormatDate(last_timestamp)
            now = datetime.now()
            if (last_timestamp - now).total_seconds() < REDIS_PHONE_TIME_GAP:
                req.msg = "发送短信过于频繁，请稍后再发"
        try:
            # 生成随机验证码
            code = "".join([str(random.randint(0, 9)) for _ in range(PHONE_CODE_LENGTH)])
            template_param = {"code": code}
            # 利用阿里云sdk发送短信
            sms = SendSms(phone=re_phone, category=category, template_param=template_param)  # TODO 考虑修改为异步程序
            sms.send_sms()

            # 利用redis存储验证码信息，用于后续的验证; 保存当前时间
            phone_key = REDIS_PHONE_CODE.format(re_phone)
            redis_conn.hset(phone_key, phone_key, code)
            now_time = getFormatDate((now + datetime.timedelta(minutes=1)))
            redis_conn.hset(phone_key, REDIS_PHONE_LAST_TIME, now_time)
            redis_conn.conn.expire(phone_key, REDIS_PHONE_CODE_EX)

            req.code = 0
            req.msg = "短信发送成功"
        except Exception as e:
            web_logger.debug(e)
            req.msg = str(e)
        return req.result

    def post(self):
        """验证手机验证码"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument("phone", type=str, required=True, loction="json", help="请输入手机号码")
        parse.add_argument("code", type=str, required=True, location="json", help="请输入短信验证码")
        front_data = parse.add_argument()

        phone = front_data.get("phone")
        code = front_data.get("code")
        re_phone = validate_phone(phone)

        phone_key = REDIS_PHONE_CODE.format(re_phone)
        right_code = redis_conn.hget(phone_key, phone_key)
        if right_code == code:
            req.code = 0
            req.msg = "验证成功"
        else:
            req.msg = "验证码不正确"

        return req.result
