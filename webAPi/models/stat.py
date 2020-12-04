# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from webAPi.models import db, Column, BaseMixin
from webAPi.utils.com import produce_id


# 记录公共项目操作执行步骤的数据表

class ActionLog(db.Model, BaseMixin):
    __tablename__ = 'action_log'
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    action = Column(db.String(120), nullable=False, comment="访问的视图函数")
    exec_status = Column(db.INTEGER, default=0, comment="执行结果：0-success  1-fail")
    log = Column(db.TEXT(120), nullable=False, comment="执行日志")

    def __init__(self, *args, **kwargs):
        # 设置id的默认值
        if kwargs.get('id') is None:
            kwargs['id'] = produce_id()
        super().__init__(*args, **kwargs)
