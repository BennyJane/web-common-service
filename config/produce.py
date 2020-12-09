# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
import logging
from .base import BaseConfig
from _compat import modifyPath
from _compat import root_path as project_root_path
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


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

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    # 日志配置
    LOG_FILE_PATH = os.path.join(project_root_path, modifyPath('logs/api/web_common.log'))
    LOG_LEVEL = logging.DEBUG
    LOG_FILE_SIZE = 10 * 1204 * 1024
    LOG_FILE_COUNT = 10

    # apscheduler 定时任务调度配置
    JOB_STORES = {
        "redis": RedisJobStore(host=REDIS_HOST, port=REDIS_PORT),  # 设置一个名为redis的job存储，后端使用 redis
        # 一个名为 default 的 job 存储，后端使用数据库（使用 Sqlite）
        # "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")
        "backend_db": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }
    JOB_EXECUTORS = {
        "default": ThreadPoolExecutor(20),  # 设置一个名为 default的线程池执行器， 最大线程设置为20个
        "processpool": ProcessPoolExecutor(4),  # 设置一个名为 processpool的进程池执行器，最大进程数设为5个
    }
    # 开启job合并，设置job最大实例上限为3
    JOB_DEFAULT = {
        'coalesce': False,
        'max_instances': 3
    }
