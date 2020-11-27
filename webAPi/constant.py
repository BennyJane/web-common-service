# -*- coding: utf-8 -*-
# @Time : 2020/11/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py


class ReqJson:
    __slots__ = ('code', 'data', 'msg')

    def __init__(self, code=0, data=None, msg=""):
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
