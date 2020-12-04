# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from flask_sqlalchemy import SQLAlchemy

from webAPi.utils.jwt import JWTManager
from webAPi.utils.redis import RedisConn

db = SQLAlchemy(use_native_unicode='utf8mb4')
jwt_manager = JWTManager()
redis_conn = RedisConn()


def register_ext(app):
    """注册扩展包"""
    db.init_app(app)
    jwt_manager.init_app(app)
    redis_conn.init_app(app)
