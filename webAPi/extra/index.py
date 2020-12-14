# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from flask_restful import Resource

from webAPi.response import ReqJson
from webAPi.utils.decorator import WhiteApi


@WhiteApi()
class Index(Resource):
    def get(self):
        req = ReqJson(code=0,
                      data={
                          "project": "公共项目",
                          "brief": "该项目独立实现了用户、文件存储、邮件、定时任务等功能模块。"
                      },
                      msg="Welcome here! This is a project to relize common functions in the development fo web.")

        return req.result
