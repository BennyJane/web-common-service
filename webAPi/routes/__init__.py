from flask import Blueprint
from flask_restful import Api

from webAPi.errors import restful_errors

api_bp = Blueprint('api', __name__)
resources_api = Api(api_bp, catch_all_404s=False, errors=restful_errors)  # catch_all_404s 必须设置为False


# 注册接口的方法完全可以写在该文件中  ==》 可以利用该方法继续拆分resources包
def register_routes_api(app):
    app.register_blueprint(api_bp, url_prefix='/api/v1')  # api必须先绑定蓝图，然后再在flask实例上注册蓝图，顺序不能变
    # FIXME 在该函数中注册 flask-restful api 会失败？？

    from webAPi.routes.index import Index
    resources_api.add_resource(Index, '/')

    from webAPi.routes.auth import Login, Logout, Register, Authenticate, GetTokenByAccount, ChangePassword, AvatarImage
    resources_api.add_resource(Login, '/auth/login')
    resources_api.add_resource(Logout, '/auth/logout')
    resources_api.add_resource(Register, '/auth/register')
    resources_api.add_resource(Authenticate, '/auth/authenticate')
    resources_api.add_resource(GetTokenByAccount, '/auth/login/account')
    resources_api.add_resource(ChangePassword, '/auth/account/reset-password')
    resources_api.add_resource(AvatarImage, '/auth/account/avatar')

    from webAPi.routes.download import DownloadImage, GetImage, LocalUploadFile
    resources_api.add_resource(LocalUploadFile, '/media/upload')
    resources_api.add_resource(DownloadImage, '/media/download')
    resources_api.add_resource(GetImage, '/media/get-image')
