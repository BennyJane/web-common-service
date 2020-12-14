# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import traceback
from flask import jsonify
from flask import current_app

from webAPi import web_logger
from webAPi.response import ReqJson


def register_errors(app):
    """"""
    # 直接调用装饰器
    app.errorhandler(400)(bad_request)
    app.errorhandler(404)(not_found)
    app.errorhandler(405)(method_not_allowed)  # todo 该异常没有捕获
    app.errorhandler(500)(internal_server_error)
    app.errorhandler(Exception)(allException)  # 全局异常捕获


def bad_request(e):
    req = ReqJson(code=1, msg="请求报错")
    return jsonify(req.result), 400


def not_found(e):
    req = ReqJson(code=1, msg="请求接口不存在")
    return jsonify(req.result), 404


def method_not_allowed(e):
    req = ReqJson(code=1, msg="请求方式不正确")
    return jsonify(req.result), 405


def internal_server_error(e):
    req = ReqJson(code=1, msg="服务器内部报错")
    return jsonify(req.result), 500


def allException(e):  # 全局异常处理
    req = ReqJson()
    req.msg = str(e)
    config = current_app.config
    if config.get("IS_DEBUG"):  # 开发模式下，打印输出异常发生的位置
        web_logger.debug(traceback.format_exc())
    return jsonify(req.result)


"""
============================================================================================================
自定义定义flask-restful的错误处理方式
============================================================================================================
"""
