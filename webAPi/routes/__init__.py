from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
resources_api = Api(api_bp)


# 注册接口的方法完全可以写在该文件中  ==》 可以利用该方法继续拆分resources包
def register_api(api):
    from commonAPi.routes.auth import Login
    from commonAPi.routes.auth import Logout
    from commonAPi.routes.auth import Register
    from commonAPi.routes.index import Index

    api.add_resource(Index, '/')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Logout, '/auth/logout')
    api.add_resource(Register, '/auth/register')
