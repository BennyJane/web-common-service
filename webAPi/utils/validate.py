# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 23:02
# Warning    ：The Hard Way Is Easier

import re
import abc


class ValidatorMeta(abc.ABC):
    """节省内存空间"""
    __slots__ = ("regex", "msg", "default")


class DataRequired(ValidatorMeta):
    """允许字段为空,并返回一个默认值"""

    def __init__(self, msg=None):
        self.msg = msg

    def __call__(self, field):
        if field is None or not field.strip():
            raise Exception(self.msg)
        return None


class AddDefault(ValidatorMeta):
    """允许字段为空,并返回一个默认值"""

    def __init__(self, default=None, msg=None):
        self.default = default
        self.msg = msg

    def __call__(self, field):
        if field is None or not field.strip():
            return self.default


"""
========================================================================================================================
正则检测类
========================================================================================================================
"""


class Regexp(object):
    def __init__(self, regex, flags=0, msg=None):
        regex = re.compile(regex, flags)
        self.regex = regex
        self.msg = msg

    def __call__(self, data, msg=None):
        match = self.regex.match(data or "")
        if not match:
            if msg is None:
                if self.msg is None:
                    msg = "无效输入"
                else:
                    msg = self.msg
            raise Exception(msg)
        return match


def validate_phone(phone):
    # TODO 优化手机号码检测方法
    phone_validate = Regexp(regex=r"^1[3-9][0-9{9}]$", msg="手机格式不正确")
    re_phone = phone_validate(phone)  # 验证手机号，并返回匹配到的号码
    return re_phone
