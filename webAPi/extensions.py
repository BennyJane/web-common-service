# -*- coding: utf-8 -*-
# @Time : 2020/11/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : web-common-service
from flask_sqlalchemy import SQLAlchemy

from webAPi.utils.jwt import JWTManager

db = SQLAlchemy()
jwt_manager = JWTManager()


def register_ext(app):
    """注册扩展包"""
    db.init_app(app)
    jwt_manager.init_app(app)
