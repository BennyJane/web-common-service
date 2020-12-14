# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 10:13
# Warning    ：The Hard Way Is Easier
from flask_restful import Resource

from webAPi.response import ReqJson

"""
实现一个API的基础类，优化ReqJson的使用方法
TODO： 将ReqJson类功能直接添加到BaseApi内，使用self.result 直接调用self.req.result的效果
"""


class BaseApi(Resource):
    """custom a base class for the api interface"""
    method_decorators = []  # 装饰器

    def __init__(self):
        self.req = ReqJson()

    @property
    def req_json(self):
        return self.req.result


if __name__ == '__main__':
    api = BaseApi()
    print(api.req_json)
