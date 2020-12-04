# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

class ResponseDescriptor:
    """存储属性与托管属性名称保持一致，可以不用实现__get__协议"""

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value
