# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

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

PHONE_CODE_LENGTH = 6  # 断线验证长度
REDIS_PHONE_CODE = "phone:code:{}"  # 短信验证码的键名称
REDIS_PHONE_CODE_EX = 60 * 5  # 短信验证码过期时间： 5分钟
REDIS_PHONE_LAST_TIME = "last_send_timestamp"  # 前一次发送短信的时间
REDIS_PHONE_TIME_GAP = 60  # 对于同一个手机号，两次短信发送间隔1分钟
