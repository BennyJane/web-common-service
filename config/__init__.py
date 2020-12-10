# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os

from .development import DevelopmentConfig
from .produce import ProduceConfig

projectConfigs = {
    "development": DevelopmentConfig,
    "produce": ProduceConfig,
}


def get_config_from_env(config_name=None):
    """根据环境变量获取当前配置信息"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in projectConfigs.keys():
            config_name = 'development'
    return projectConfigs[config_name]
