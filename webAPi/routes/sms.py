# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 23:34
# Warning    ：The Hard Way Is Easier
import datetime
from flask_restful import Resource
from flask_restful import reqparse
from webAPi.response import ReqJson
from webAPi.extensions import redis_conn
from webAPi.utils.validate import Regexp
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
        # TODO 检测手机格式：长度13位，数值类型
        phone_validate = Regexp(regex=r"^1[3-9][0-9{9}]$", msg="手机格式不正确")
        re_phone = phone_validate(phone)  # 验证手机号，并返回匹配到的号码

        # 限制短信发送频率
        last_timestamp = redis_conn.hget(re_phone, REDIS_PHONE_LAST_TIME)
        if last_timestamp is not None:
            last_timestamp =

    def post(self):
        """验证手机验证码"""
