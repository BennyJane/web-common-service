# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from webAPi.utils.jwt import JWTManager
from webAPi.utils.redis import RedisConn

from webAPi.utils.cron_libs import CronScheduler

mail = Mail()
csrf = CORS()
redis_conn = RedisConn()
jwt_manager = JWTManager()
cron_scheduler = CronScheduler()
db = SQLAlchemy(use_native_unicode='utf8mb4')


def register_ext(app):
    """注册扩展包"""
    db.init_app(app)
    jwt_manager.init_app(app)
    redis_conn.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    cron_scheduler.init_app(app)
