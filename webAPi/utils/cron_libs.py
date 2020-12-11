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
        conf = {  # redis配置
            "host": config.REDIS_HOST,
            "port": config.REDIS_PORT,
            "db": 15,  # 连接15号数据库
            "max_connections": 10  # redis最大支持300个连接数
        }
        job_stores = {
            'redis': RedisJobStore(**conf)
        }
        self.scheduler = BackgroundScheduler(
            jobstores=job_stores,
            executors=config.JOB_EXECUTORS,
            job_default=config.JOB_DEFAULT,
            timezone='Asia/Shanghai'
        )

    def init_app(self, app):
        """绑定实例Flask 实例"""
        app.cron_scheduler = self
        self.run()

    def add_task(self, params: dict):
        if params.get("loop") == 'date':
            self.one_off_task(params)
        elif params.get('loop') == 'interval':
            self.interval_task(params)
        elif params.get('loop') == 'cron':
            self.periodic_task(params)
        else:
            web_logger.error("没有找到任务类型")

    def periodic_task(self, params: dict):
        """周期性任务"""
        valid_date = get_date(params.get("cron"))

        self.scheduler.add_job(
            self.task.request_get,
            jobstore='redis',
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
            jobstore='redis',
            max_instances=1,  # 同id，允许任务数量
            trigger='date',
            run_date=cron_date(params.get("cron")),
            args=(params.get("callback_url"),),
        )

    def interval_task(self, params: dict):
        """按照指定间隔，重复执行任务"""
        self.scheduler.add_job(
            self.task.request_get,
            jobstore='redis',
            max_instances=1,  # 同id，允许任务数量
            trigger='interval',
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
        # 先判断是否有暂定的任务
        self.scheduler.print_jobs()
        all_jobs = get_cron_tasks()
        self.scheduler.print_jobs()
        for params in all_jobs:
            try:
                self.add_task(params)
            except Exception as e:
                web_logger.error(e)

    def run(self):
        """添加锁机制"""
        # TODO 添加锁机制，解决多线程与多进程下任务重复执行的BUG
        try:
            self.scheduler.start()  # 使用 redis存储后，任务后自动重启
        except Exception as e:
            web_logger.error(e)

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
        # 局部导入，避免包导入的错误
        from webAPi.extensions import redis_conn
        from webAPi.utils.redis import redis_lock
        with redis_lock(redis_conn.conn, "request_get") as lock:
            # 使用redis锁，确保任务触发时，该方法只执行一次，因为只有一个线程能执行成功
            if not lock:
                return
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    # TODO 记录任务失败的信息
                    web_logger.debug(f"status_code:{res.status_code} {res.text}")
                web_logger.info("request get running...")
            except Exception as e:
                web_logger.info(e)

    def test_write_file(self):
        number = random.randint(0, 100)
        with open('./record.txt', 'a') as f:
            f.write(f"random num: {number}")
