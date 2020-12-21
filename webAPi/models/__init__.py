# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from datetime import datetime
from webAPi.extensions import db
from webAPi.utils.com import produce_id

Column = db.Column


class BaseMixin(object):  # 参考superset项目
    # TODO datetime.utctime 时间不是北京时间
    create_at = Column(db.DateTime, default=datetime.now)
    update_at = Column(db.DateTime, default=datetime.now)

    @property
    def create_time_str(self, formatter="%Y-%m-%d %H:%M:%S"):
        return self.create_at.strftime(formatter)

    @property
    def update_time_str(self, formatter="%Y-%m-%d %H:%M:%S"):
        return self.create_at.strftime(formatter)

    @property
    def attr_dict(self) -> dict:
        """实现获取ORM定义的字段信息，并将其转化为字典格式输出"""
        print('attr dict', vars(self.__class__))


class BaseModel(db.Model):
    """数据库基类：抽象类，不会创建数据表"""
    __abstract__ = True

    id = Column(db.String(32), default=produce_id, primary_key=True)  # 所有表统一设置ID值


from .user import User
from .appInfo import AppInfo
from .download import Downloading
from .mail import MailTemplate
from .stat import ActionLog
from .cron import Cron
