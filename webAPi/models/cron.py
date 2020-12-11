# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/9 0:40
# Warning    ：The Hard Way Is Easier
import json
from webAPi.extensions import db
from webAPi.models import Column
from webAPi.log import web_logger
from webAPi.models import BaseMixin
from webAPi.utils.com import produce_id


class Cron(db.Model, BaseMixin):
    __tablename__ = 'cron'

    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    crontab = Column(db.TEXT, default="", comment="任务执行时间配置")
    callback_url = Column(db.TEXT, default="")
    next_run_date = Column(db.String(32), default="")
    loop = Column(db.String(32), default='cron', comment="date:指定时间执行一次；cron:特定时间定期执行；interval: 按照指定间隔重复执行")
    status = Column(db.INTEGER, default=0, comment="0:未执行；1： 进行中； 2： 失败； 3： 成功")  # 目前没有使用
    description = Column(db.TEXT, default="")
    try_count = Column(db.INTEGER, default=0, comment="失败重试次数")

    def __init__(self, *args, **kwargs):
        # 设置id的默认值
        if kwargs.get('id') is None:
            kwargs['id'] = produce_id()
        crontab_value = kwargs.get("crontab")
        if crontab_value is not None and not isinstance(crontab_value, str):
            kwargs['crontab'] = json.dumps(crontab_value, ensure_ascii=False)
        super().__init__(*args, **kwargs)

    def get_params(self):
        params = {
            "job_id": self.id,
            "cron": json.loads(self.crontab),
            "callback_url": self.callback_url,
            "loop": self.loop
        }
        return params

    @staticmethod
    def restart_task(cron_scheduler=None):
        """项目初始化时，启动所有定时任务"""
        # FIXME 这块代码在项目启动的时候，被执行了两遍
        cron_scheduler.scheduler.remove_all_jobs()  # 先删除当前的所有的任务
        all_tasks = Cron.query.all()
        web_logger.info("重新启动所有定时任务")
        web_logger.info("当前定时任务数量： {}".format(len(all_tasks)))
        for task in all_tasks:
            params = task.get_params()
            cron_scheduler.add_task(params)
