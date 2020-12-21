# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from webAPi.models import db
from webAPi.models import Column
from webAPi.models import BaseModel
from webAPi.models import BaseMixin


class Downloading(BaseModel, BaseMixin):
    __tablename__ = 'downloading'
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    name = Column(db.String(120), nullable=False, comment="文件原始名称")
    file_type = Column(db.String(120), nullable=False, comment="上传文件的类型")
