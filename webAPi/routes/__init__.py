from flask import Blueprint, jsonify
from flask_restful import Api

from webAPi.constant import ReqJson

api_bp = Blueprint('api', __name__)
resources_api = Api(api_bp, catch_all_404s=True)


@api_bp.errorhandler(405)
def method_not_allowed(e):
    req = ReqJson(code=1, msg="请求方式不正确")
    return jsonify(req.result), 405


# 注册接口的方法完全可以写在该文件中  ==》 可以利用该方法继续拆分resources包
def register_routes_api(app):
    app.register_blueprint(api_bp, url_prefix='/api/v1')  # api必须先绑定蓝图，然后再在flask实例上注册蓝图，顺序不能变
    from webAPi.routes.auth import Login
    from webAPi.routes.auth import Logout
    from webAPi.routes.auth import Register
    from webAPi.routes.index import Index

    resources_api.add_resource(Index, '/')
    resources_api.add_resource(Login, '/auth/login')
    resources_api.add_resource(Logout, '/auth/logout')
    resources_api.add_resource(Register, '/auth/register')
