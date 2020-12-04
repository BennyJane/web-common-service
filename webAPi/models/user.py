# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from flask import current_app
from sqlalchemy import and_

from webAPi.models import db
from webAPi.models import Column
from webAPi.models import BaseMixin
from webAPi.utils.com import produce_id


class User(db.Model, BaseMixin):
    __tablename__ = 'user'
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    account = Column(db.String(120), nullable=False, comment="用户账号的唯一标识")
    password = Column(db.Text, nullable=False)
    status = Column(db.Integer, default=0, comment="账号状态：0 可用/1 不可用")

    def __init__(self, *args, **kwargs):
        # 设置id的默认值
        if kwargs.get('id') is None:
            kwargs['id'] = produce_id()
        super().__init__(*args, **kwargs)

    @staticmethod
    def insert_test_user():
        config = current_app.config
        test_account = config.get("TEST_ACCOUNT")
        test_password = config.get("TEST_PASSWORD")
        test_app_id = config.get("TEST_APP_ID")
        user = User.query.filter(and_(User.account == test_account,
                                      User.app_id == test_app_id)).first()
        if not user:
            test_user = User(id=produce_id(), app_id=test_app_id, account=test_account,
                             password=test_password)
            db.session.add(test_user)
            db.session.commit()
