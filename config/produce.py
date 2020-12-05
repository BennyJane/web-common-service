# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
from .base import BaseConfig, prefix, project_root_path


class ProduceConfig(BaseConfig):
    # 本项目使用的域名与端口号
    PROJECT_PORT = 5000
    PROJECT_DOMAIN = f"http://localhost:{PROJECT_PORT}"

    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(project_root_path, 'data-produce.db')
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{MYSQL_PASSWORD}@127.0.0.1:13306/common_web_service?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENCODING = "utf8mb4"

    # 添加celery配置
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    imports = ('proStruct.services.tasks')
