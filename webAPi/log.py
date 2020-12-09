# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
import logging
from logging.handlers import RotatingFileHandler

from config import projectConfigs

"""
基于flask中自带的logger来设计日志模式
"""


def get_settings(config):
    # print('config vas', vars(config))
    # path = getattr(config, "LOG_FILE_PATH")
    # level = getattr(config, "LOG_LEVEL")
    # size = getattr(config, "LOG_FILE_SIZE")
    # count = getattr(config, "LOG_FILE_COUNT")

    path = config.get("LOG_FILE_PATH")
    level = config.get("LOG_LEVEL")
    size = config.get("LOG_FILE_SIZE")
    count = config.get("LOG_FILE_COUNT")
    # print(path, level, size, count)
    return path, level, size, count


def register_logger(app):
    config = app.config
    log_file_path, log_level, log_file_size, log_file_count = get_settings(config)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=log_file_count)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    if not app.debug:  # 非调试模式下，才添加日志文件
        app.logger.addHandler(file_handler)


# TODO 单独定义邮件发送使用的日志 ==》 不能使用flask自带的日志


def get_logger(config_name=None):
    if config_name is None:
        current_env = os.getenv('FLASK_ENV', 'development')
        if current_env not in projectConfigs.keys():
            config_name = 'development'
        else:
            config_name = current_env
    config_object = projectConfigs[config_name]
    log_file_path = config_object.LOG_FILE_PATH
    log_level = config_object.LOG_LEVEL
    log_file_size = config_object.LOG_FILE_SIZE
    log_file_count = config_object.LOG_FILE_COUNT

    logger = logging.getLogger(__name__)

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s [%(module)s.%(filename)s] [%(levelname)s] : %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    if log_file_path and current_env == 'produce':
        handler = logging.FileHandler(log_file_path)
    elif log_level is None:
        logger.handlers = [logging.NullHandler()]
        return logger
    if current_env == 'development':
        handler = logging.StreamHandler()

    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    return logger


# 利用python模块实现单例
web_logger = get_logger()
