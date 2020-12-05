# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os

from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    # 本项目使用的域名与端口号
    PROJECT_PORT = 5000
    PROJECT_DOMAIN = f"http://localhost:{PROJECT_PORT}"


    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(project_root_path, 'data-dev.db')
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{MYSQL_PASSWORD}@127.0.0.1:13306/common_web_service?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENCODING = "utf8mb4"

    # 添加celery配置
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    imports = ('proStruct.services.tasks')

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    # 测试账号
    TEST_APP_ID = 'dc601e113be8a2e622f9f9a3f363eb93'
    TEST_ACCOUNT = '15845623256'
    TEST_PASSWORD = '8b18762706f0c6854d967b6bb36a97df318654f44b9fe007078149759f25f9d2'  # aaasss123
