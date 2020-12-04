# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import json
from flask import g
from collections import namedtuple
from webAPi.extensions import db
from webAPi.models import Column
from webAPi.models import BaseMixin
from webAPi.utils.com import produce_id
from webAPi.constant import UPLOAD_FILE_BASE_CONF

APP_INFO = namedtuple('app_info', 'id name brief status conf')


class AppInfo(db.Model, BaseMixin):
    __tablename__ = 'app_info'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    id = Column(db.String(32), primary_key=True)
    name = Column(db.String(255), nullable=False, comment="应用名称")
    brief = Column(db.Text, nullable=False, comment="应用简介")
    status = Column(db.Integer, default=0, comment="应用状态：0 可用/1 不可用")
    conf = Column(db.Text, nullable=False, comment="使用json存储上传文件的配置信息")

    @staticmethod
    def insert_data():
        app_infos = [
            APP_INFO('dc601e113be8a2e622f9f9a3f363eb93', 'test_project', '这是一个测试项目', 0, UPLOAD_FILE_BASE_CONF),
            APP_INFO('1b4925bfa780f5964a2de19e5322dca4', 'school_info', '学校信息网', 0, UPLOAD_FILE_BASE_CONF),
        ]
        for info in app_infos:
            app = AppInfo.query.filter_by(name=info.name).first()
            # 对于已经存在的项目数据，只通过接口更新
            if app is None:
                app_id = info.id if info.id else produce_id()
                app = AppInfo(id=app_id, name=info.name, brief=info.brief,
                              status=info.status, conf=json.dumps(info.conf, ensure_ascii=False))
                db.session.add(app)
                db.session.commit()

    @property
    def upload_conf(self):
        return json.loads(self.conf)

    @staticmethod
    def get_app_info():
        app_id = g.app_id
        app_info = AppInfo.query.get(app_id)
        return app_info
