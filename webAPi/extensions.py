# -*- coding: utf-8 -*-
# @Time : 2020/11/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : web-common-service
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def register_ext(app):
    """注册扩展包"""
    db.init_app(app)
