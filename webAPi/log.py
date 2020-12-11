# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
import logging
from config import get_config_from_env
from logging.handlers import RotatingFileHandler


# TODO 单独定义邮件发送使用的日志 ==》 不能使用flask自带的日志


def get_logger(config_name=None):
    current_env = os.getenv('FLASK_ENV', 'development')
    config = get_config_from_env()
    log_file_path = config.LOG_FILE_PATH
    log_level = config.LOG_LEVEL
    log_file_size = config.LOG_FILE_SIZE
    log_file_count = config.LOG_FILE_COUNT

    logger = logging.getLogger(config.PROJECT_NAME)

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s [%(module)s.%(filename)s %(lineno)s] [%(levelname)s] : %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    if log_file_path and current_env == 'produce':
        handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=log_file_count)
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
