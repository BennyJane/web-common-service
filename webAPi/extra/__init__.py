# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from webAPi.extensions import Api


def register_extra_api(app):
    extra_api = Api(app)
    from .index import Index
    extra_api.add_resource(Index, '/')
