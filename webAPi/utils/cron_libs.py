# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/9 1:26
# Warning    ：The Hard Way Is Easier
import random
import datetime
import requests
from pytz import utc
from webAPi.log import web_logger
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler


class CronScheduler:
    scheduler = None

    def __init__(self):
        """初始化任务功能"""
        self.task = CronTask()

    def init_app(self, app):
        """绑定实例，读取配置文件"""
        config = app.config
        self.scheduler = BackgroundScheduler(
            jobstores=config.get("JOB_STORES"),
            executors=config.get("JOB_EXECUTORS"),
            job_default=config.get("JOB_DEFAULT"),
            timezone=utc
        )
        self.scheduler.start()

    def add_task(self, params: dict):
        if params.get("loop") == 0:
            self.one_off_task(params)
        else:
            self.periodic_task(params)

    def periodic_task(self, params: dict):
        """周期性任务"""
        self.scheduler.add_job(
            self.task.request_get,
            trigger='cron',
            id=params.get("job_id"),
            year=params.get("year"),
            month=params.get("month"),
            day=params.get("day"),
            hour=params.get("hour"),
            minute=params.get("minute"),
            second=params.get("second"),
            args=(params.get("callback_url"),),
        )
        web_logger.info("add periodic task...")

    def one_off_task(self, params: dict):
        """只在指定时间，执行一次的任务"""
        self.scheduler.add_job(
            self.task.request_get,
            trigger='date',
            run_date=cron_date(params.get("cron")),
            args=(params.get("callback_url"),),
        )

    def delete_task(self, job_id):
        """删除任务"""
        try:
            self.scheduler.remove_job(job_id=job_id)
        except JobLookupError as e:
            # 任务不存在
            pass
        except Exception as e:
            raise Exception(str(e))

class CronTask:

    def request_get(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            # TODO 记录任务失败的信息
            web_logger.debug(f"status_code:{res.status_code} {res.text}")
        print("request get running...")

    def test_write_file(self):
        number = random.randint(0, 100)
        with open('./record.txt', 'a') as f:
            f.write(f"random num: {number}")
