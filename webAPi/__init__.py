# -*- coding: utf-8 -*-
# @Time : 2020/11/26
# @Author : Benny Jane
# @Email : 暂无
import os

from flask import Flask

from config import projectConfigs
from webAPi.errors import register_errors
from webAPi.extra import extra_bp, extra_api
from webAPi.extra import register_extra_api
from webAPi.models import *  # 导入所有数据表
from webAPi.routes import resources_api, register_routes_api
from webAPi.routes.index import Index
from .extensions import register_ext, db


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in projectConfigs.keys():
            config_name = 'development'
    app = Flask(__name__)
    app.config.from_object(projectConfigs[config_name])

    register_errors(app)  # 处理异常情况

    register_routes_api(app)  # 核心接口定义
    register_extra_api(app)  # 次要接口定义

    register_ext(app)  # 绑定扩展包
    with app.app_context():  # 必须在app的上下文中，才能执行创建数据库的操作
        # db.drop_all()
        db.create_all()
        AppInfo.insert_data()

    return app  # todo　必须返回Flask实例
