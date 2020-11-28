# -*- coding: utf-8 -*-
# @Time : 2020/11/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py


class ReqJson:
    __slots__ = ('_code', '_data', '_msg',)

    def __init__(self, code=1, data=None, msg=""):
        self._code = code
        self._data = {} if data is None else data
        self._msg = msg

    @property
    def code(self):
        return self._code

    @property
    def data(self):
        return self._data

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @data.setter
    def data(self, value):
        self._data = value

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def result(self):
        return {
            "code": self.code,
            "data": self.data,
            "msg": self.msg,
        }


class HttpCode:
    """"""
