# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
from .base import BaseConfig, prefix, project_root_path


class ProduceConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(project_root_path, 'data-produce.mysql')

    # 添加celery配置
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    imports = ('proStruct.services.tasks')
