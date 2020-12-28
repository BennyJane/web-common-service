# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from flask_mail import Mail
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from webAPi.utils.jwt import JWTManager
from webAPi.utils.com import error_router
from webAPi.utils.redis_libs import RedisConn
from webAPi.utils.cron_libs import CronScheduler

mail = Mail()
csrf = CORS()
migrate = Migrate()
redis_conn = RedisConn()
jwt_manager = JWTManager()
cron_scheduler = CronScheduler()
db = SQLAlchemy(use_native_unicode='utf8mb4')


def register_ext(app):
    """注册扩展包"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    redis_conn.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)  # 解决跨域问题
    cron_scheduler.init_app(app)


# 重写error_router类方法，修改flask-restful内部处理异常的返回格式
Api.error_router = error_router
