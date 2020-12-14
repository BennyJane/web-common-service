# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

from flask import Blueprint

from webAPi.extensions import Api

api_bp = Blueprint('api', __name__)


# 注册接口的方法完全可以写在该文件中  ==》 可以利用该方法继续拆分resources包
def register_routes_api(app):
    resources_api = Api(api_bp, catch_all_404s=False)  # catch_all_404s 必须设置为False
    app.register_blueprint(api_bp, url_prefix='/api/v1')  # api必须先绑定蓝图，然后再在flask实例上注册蓝图，顺序不能变

    from webAPi.routes.index import Index
    # FIXME 如何定义该接口，消除末尾的/
    resources_api.add_resource(Index, '/')  # http://127.0.0.1:5000/api/v1/ 末尾必须添加/

    from webAPi.routes.auth import Login, Logout, Register, Authenticate, \
        GetTokenByAccount, ChangePassword, AvatarImage, Captcha

    resources_api.add_resource(Login, '/auth/login')
    resources_api.add_resource(Logout, '/auth/logout')
    resources_api.add_resource(Register, '/auth/register')
    resources_api.add_resource(Authenticate, '/auth/authenticate')
    resources_api.add_resource(GetTokenByAccount, '/auth/login/account')
    resources_api.add_resource(ChangePassword, '/auth/account/reset-password')
    resources_api.add_resource(AvatarImage, '/auth/account/avatar')
    resources_api.add_resource(Captcha, '/auth/captcha')

    from webAPi.routes.download import DownloadImage, GetImage, LocalUploadFile, UpdateFileConf
    resources_api.add_resource(LocalUploadFile, '/media/upload')
    resources_api.add_resource(DownloadImage, '/media/download')
    resources_api.add_resource(GetImage, '/media/get-image')
    resources_api.add_resource(UpdateFileConf, '/media/update/file/conf')

    from webAPi.routes.mail import MailConf, SimpleSendMail, AddMail
    resources_api.add_resource(MailConf, '/mail/templates')
    resources_api.add_resource(AddMail, '/mail/task')
    resources_api.add_resource(SimpleSendMail, '/mail/task/execute')

    from webAPi.routes.cron import CronTask
    resources_api.add_resource(CronTask, '/cron/task')

    from webAPi.routes.sms import Sms
    resources_api.add_resource(Sms, "/sms")
