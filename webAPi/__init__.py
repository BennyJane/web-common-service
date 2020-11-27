# -*- coding: utf-8 -*-
# @Time : 2020/11/26
# @Author : Benny Jane
# @Email : 暂无
import os
from flask import Flask
from config import projectConfigs
from webAPi.extra import extra_bp, extra_api
from webAPi.extra.other import Other
from webAPi.routes import api_bp, resources_api
from webAPi.routes.auth import Login, Logout, Register
from webAPi.routes.index import Index


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in projectConfigs.keys():
            config_name = 'development'
    app = Flask(__name__)
    app.config.from_object(projectConfigs[config_name])

    app.register_blueprint(api_bp, url_prefix='/api/v1')  # api必须先绑定蓝图，然后再在flask实例上注册蓝图，顺序不能变
    app.register_blueprint(extra_bp, url_prefix='/api/v1/extra')

    resources_api.add_resource(Index, '/')
    resources_api.add_resource(Login, '/auth/login')
    resources_api.add_resource(Logout, '/auth/logout')
    resources_api.add_resource(Register, '/auth/register')

    # extra
    extra_api.add_resource(Other, '/')

    return app  # todo　必须返回Flask实例
