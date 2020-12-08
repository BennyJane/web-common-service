# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/9 0:40
# Warning    ：The Hard Way Is Easier
from webAPi.models import db
from webAPi.models import Column
from webAPi.models import BaseMixin
from webAPi.utils.com import produce_id


class Cron(db.Model, BaseMixin):
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    crontab = Column(db.String(60), default="", comment="任务执行时间配置")
    callback_url = Column(db.TEXT, default="")
    next_run_date = Column(db.String(32), default="")
    loop = Column(db.INTEGER, default=0, comment="0:不循环，只执行一次；1:循环")
    status = Column(db.INTEGER, default=0, comment="0:未执行；1： 进行中； 2： 失败； 3： 成功")
    description = Column(db.TEXT, default="")
    try_count = Column(db.INTEGER, default=0, comment="失败重试次数")
