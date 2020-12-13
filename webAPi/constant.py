# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from webAPi.utils.descriptor import ResponseDescriptor


class ReqJson:
    # 使用描述符管理实例属性
    code = ResponseDescriptor("code")
    data = ResponseDescriptor("data")
    msg = ResponseDescriptor("msg")

    def __init__(self, code=-1, data=None, msg=""):
        self.code = code
        self.data = {} if data is None else data
        self.msg = msg

    @property
    def result(self):
        return {
            "code": self.code,
            "data": self.data,
            "msg": self.msg,
        }


class HttpCode:
    """"""


REDIS_REFRESH_TOKEN_KEY = "{}:refresh_token"

UPLOAD_FILE_BASE_CONF = {
    "allow_file_types": ["image", "doc"],
    "image": {
        "max_content_size": 1024 * 1024 * 3,  # 默认文件最大为3M
        "allow_extensions": ["png", 'jpg', 'gif', 'webp'],  # 允许上传的文件后缀名
    },
    "doc": {
        "max_content_size": 1024 * 1024 * 5,  # 默认文件最大为5M
        "allow_extensions": ['doc', 'docx', 'pdf', 'csv', 'xls'],  # 允许上传的文件后缀名
    },
    "video": {
        "max_content_size": 1024 * 1024 * 20,  # 默认文件最大为20M
        "allow_extensions": [],  # 允许上传的文件后缀名
    },
}

REDIS_MAIL_QUEUE = "mail:produce:queue"  # 邮件队列的键名称
REDIS_MAIL_INTERVAL = 2  # 邮件发送的时间间隔
