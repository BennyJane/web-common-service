# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from webAPi.models import db, Column, BaseMixin
from webAPi.utils.com import produce_id


class MailTemplate(db.Model, BaseMixin):
    __tablename__ = 'mail_template'
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    alias = Column(db.String(255), nullable=False, comment="邮件模板别名")
    subject = Column(db.String(255), nullable=False, comment="邮件主题")
    template = Column(db.TEXT, nullable=False, comment="邮件模板")

    def __init__(self, *args, **kwargs):
        # 设置id的默认值
        if kwargs.get('id') is None:
            kwargs['id'] = produce_id()
        super().__init__(*args, **kwargs)
