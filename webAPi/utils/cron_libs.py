# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/9 1:26
# Warning    ：The Hard Way Is Easier
# import atexit
# import fcntl
import random
import requests
from webAPi.log import web_logger
from webAPi.utils.com import cron_date
from webAPi.utils._threadAndprocess import _acquireLock
from webAPi.utils._threadAndprocess import _releaseLock
from webAPi.utils.com import get_config_from_env
from webAPi.utils.sql_libs import get_cron_tasks
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler


def get_date(params: dict):
    valid_date = {}
    for key, value in params.items():
        if value != '*':
            valid_date[key] = value
    web_logger.info("[定时任务时间设置]: {}".format(valid_date))
    return valid_date


class CronScheduler:
    scheduler = None

    def __init__(self):
        """初始化任务功能"""
        self.task = CronTask()
        config = get_config_from_env()
        job_stores = {
            'redis': RedisJobStore()
        }
        self.scheduler = BackgroundScheduler(
            jobstores=job_stores,
            executors=config.JOB_EXECUTORS,
            job_default=config.JOB_DEFAULT,
            timezone='Asia/Shanghai'
            # timezone=utc
        )

    def init_app(self, app):
        """绑定实例，读取配置文件: 该方法在多进程下会重复执行任务"""

    def add_task(self, params: dict):
        if params.get("loop") == 0:
            self.one_off_task(params)
        else:
            self.periodic_task(params)

    def periodic_task(self, params: dict):
        """周期性任务"""
        valid_date = get_date(params.get("cron"))

        self.scheduler.add_job(
            self.task.request_get,
            max_instances=1,  # 同id，允许任务数量
            trigger='cron',
            id=params.get("job_id"),
            args=(params.get("callback_url"),),
            **valid_date
        )

    def one_off_task(self, params: dict):
        """只在指定时间，执行一次的任务"""
        self.scheduler.add_job(
            self.task.request_get,
            max_instances=1,  # 同id，允许任务数量
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

    def restart_tasks(self):
        self.scheduler.remove_all_jobs()  # 先删除当前的所有的任务
        all_tasks = get_cron_tasks()
        web_logger.info("重新启动所有定时任务")
        web_logger.info("当前定时任务数量： {}".format(len(all_tasks)))
        for params in all_tasks:
            _acquireLock()
            try:
                self.add_task(params)
            except Exception as e:
                web_logger.error(e)
            finally:
                _releaseLock()

    def run(self):
        """添加锁机制"""
        # TODO 添加锁机制，解决多线程与多进程下任务重复执行的BUG
        _acquireLock()
        try:
            self.scheduler.start()
            # self.restart_tasks()
        except Exception as e:
            web_logger.error(e)
        finally:
            _releaseLock()

        # f = open("scheduler.lock", "wb")
        # try:
        #     fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        #     self.update()
        #     self.scheduler.start()
        # except:
        #     pass
        #
        # def unlock():
        #     fcntl.flock(f, fcntl.LOCK_UN)
        #     f.close()
        #
        # atexit.register(unlock)


class CronTask:

    def request_get(self, url):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                # TODO 记录任务失败的信息
                web_logger.debug(f"status_code:{res.status_code} {res.text}")
            web_logger.info("request get running...")
        except Exception as e:
            web_logger.info(str(e))

    def test_write_file(self):
        number = random.randint(0, 100)
        with open('./record.txt', 'a') as f:
            f.write(f"random num: {number}")
