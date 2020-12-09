# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
from flask import Flask
from webAPi.models import *  # 导入所有数据表
from config import projectConfigs
from webAPi.extensions import db
from webAPi.extensions import cron_scheduler
from webAPi.routes.index import Index
from webAPi.routes import register_routes_api
from webAPi.log import register_logger
from webAPi.extensions import register_ext
from webAPi.extra import register_extra_api
from webAPi.errors import register_errors
from webAPi.utils.decorator import register_before_after


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in projectConfigs.keys():
            config_name = 'development'
    config_object = projectConfigs[config_name]
    app = Flask(__name__, static_folder=config_object.UPLOAD_PATH)
    app.config.from_object(config_object)

    register_before_after(app)

    register_routes_api(app)  # 核心接口定义
    register_extra_api(app)  # 次要接口定义

    register_ext(app)  # 绑定扩展包
    with app.app_context():  # 必须在app的上下文中，才能执行创建数据库的操作
        # db.drop_all()
        db.create_all()
        AppInfo.insert_data()
        User.insert_test_user()
        Cron.restart_task(cron_scheduler)

    register_errors(app)  # 处理异常情况
    register_logger(app)
    return app  # todo　必须返回Flask实例
