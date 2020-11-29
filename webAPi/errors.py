import sys

from flask import jsonify

from .constant import ReqJson


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


def allException(e):
    req = ReqJson()
    req.msg = str(e)
    print(e)
    print(sys.exc_info())
    return jsonify(req.result)


"""
============================================================================================================
定义flask-restful的错误处理方式
============================================================================================================
"""
restful_errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
    'FieldParseError': {
        'msg': "A resource with that ID no longer exists.",
        'status': 400,
        'code': 1,
    },
}

"""
============================================================================================================
处理 flask-restful抛出的字段解析错误
============================================================================================================
"""


def register_teardown_request(app):
    app.teardown_request(dealError)


def dealError(response):
    return response
