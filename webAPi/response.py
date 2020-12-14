# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 23:07
# Warning    ：The Hard Way Is Easier
from webAPi.utils.descriptor import ResponseDescriptor


class ReqJson:
    # 使用描述符管理实例属性
    code = ResponseDescriptor("code")
    data = ResponseDescriptor("data")
    msg = ResponseDescriptor("msg")

    def __init__(self, code=-1, data=None, msg=""):
        self.code = code
        self.data = {} if data is None else data
        self.msg = msg

    @property
    def result(self):
        return {
            "code": self.code,
            "data": self.data,
            "msg": self.msg,
        }


class HttpCode:
    """"""
