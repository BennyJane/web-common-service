# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from flask_restful import Api

from webAPi.extensions import change_api_response


def register_extra_api(app):
    extra_api = Api(app)
    change_api_response(extra_api)
    # extra_api.init_app(app)  # 这样的定义方式不起作用
    from .index import Index
    extra_api.add_resource(Index, '/')
