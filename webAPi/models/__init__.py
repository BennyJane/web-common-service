# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from datetime import datetime
from webAPi.extensions import db

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


from .user import User
from .appInfo import AppInfo
from .download import Downloading
from .mail import MailTemplate
from .stat import ActionLog
