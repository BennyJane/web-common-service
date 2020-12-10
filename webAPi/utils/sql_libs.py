# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/10 19:15
# Warning    ：The Hard Way Is Easier

from sqlalchemy.engine import create_engine

from webAPi.log import web_logger
from webAPi.utils.com import cron_params
from webAPi.utils.com import get_config_from_env


def get_cron_tasks():
    all_tasks = []
    config = get_config_from_env()
    sqlalchemy_url = config.SQLALCHEMY_DATABASE_URI
    try:
        engine = create_engine(sqlalchemy_url, echo=False)
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute("select `id`, `crontab`,`callback_url`,`loop` from cron")
        all_tasks = cursor.fetchall()
    except Exception as e:
        web_logger.error(e)
    if all_tasks:
        all_tasks = [cron_params(item) for item in all_tasks]
    return all_tasks
