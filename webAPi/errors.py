from flask import jsonify

from .constant import ReqJson


def register_errors(app):
    """"""
    # 直接调用装饰器
    app.errorhandler(400)(bad_request)
    app.errorhandler(404)(not_found)
    app.errorhandler(405)(method_not_allowed)  # 该异常没有捕获
    app.errorhandler(500)(internal_server_error)
    # app.errorhandler(Exception)(allException)


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
    print(e)
    return ""


"""
============================================================================================================
定义flask-restful的错误处理方式
============================================================================================================
"""
restful_errors = {
    ""
}
