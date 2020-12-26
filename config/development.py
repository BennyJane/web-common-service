# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
import logging

import redis
from dotenv import load_dotenv
from .base import BaseConfig
from _compat import win
from _compat import modifyPath
from _compat import root_path as project_root_path
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.executors.pool import ProcessPoolExecutor

load_dotenv(".env")

if win:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class DevelopmentConfig(BaseConfig):
    # MYSQL数据链接
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:  # 没有添加mysql数据库连接时，创建sqlite数据库连接
        SQLALCHEMY_DATABASE_URI = prefix + os.path.join(project_root_path, 'data-dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENCODING = "utf8mb4"

    # 配置redis链接  带密码： redis://[:password]@127.0.0.1:6379/0
    REDIS_URI = os.getenv("REDIS_URI")
    if not REDIS_URI:
        # 本地redis连接URI
        REDIS_URI = f'redis://:life123456@127.0.0.1:6379/1'

    # 测试账号
    TEST_APP_ID = 'dc601e113be8a2e622f9f9a3f363eb93'
    TEST_ACCOUNT = '15845623256'
    TEST_PASSWORD = '8b18762706f0c6854d967b6bb36a97df318654f44b9fe007078149759f25f9d2'  # aaasss123

    # 日志配置: 线上需要重新设置
    LOG_FILE_PATH = os.path.join(project_root_path, modifyPath('logs/api/web_common.log'))
    LOG_LEVEL = logging.INFO
    LOG_FILE_SIZE = 10 * 1204 * 1024
    LOG_FILE_COUNT = 10

    """
    ====================================================================================================================
    添加apscheduler定时任务调度配置
    ====================================================================================================================
    """
    pools = redis.ConnectionPool.from_url(REDIS_URI)
    connect_args = dict(connection_pool=pools)
    JOB_STORES = {
        'redis': RedisJobStore(**connect_args)
    }

    JOB_EXECUTORS = {
        "default": ThreadPoolExecutor(1),  # 设置一个名为 default的线程池执行器， 最大线程设置为20个
        # TODO 线程过多，会出现同一个任务被多次执行的情况
        "processpool": ProcessPoolExecutor(1),  # 设置一个名为 processpool的进程池执行器，最大进程数设为5个
    }
    # 开启job合并，设置job最大实例上限为3
    JOB_DEFAULT = {
        'coalesce': False,
        'max_instances': 3
    }

    """
    ====================================================================================================================
    添加celery配置
    ====================================================================================================================
    """
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    imports = ('proStruct.services.tasks')
