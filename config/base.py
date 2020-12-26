# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
from _compat import win
from _compat import root_path as project_root_path

prefix = 'sqlite:////'  # linux 下前缀
if win:
    prefix = 'sqlite:///'


class BaseConfig:
    PROJECT_NAME = "web-common-service"
    PROJECT_ROOT_PATH = project_root_path
    HOST = 8020

    SESSION_KEY = 'BENNY JANE'
    IS_DEBUG = True

    SQLITE_PREFIX = prefix
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX + ':memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # 支持上传的文件类型
    UPLOAD_TYPE = ('image', 'doc', 'video')
    UPLOAD_ALLOW_TYPE = {
        "image": ("png", 'jpg', 'gif', 'webp'),
        "doc": ('doc', 'docx', 'pdf', 'csv', 'xls'),
        "video": (),
    }

    UPLOAD_PATH = os.path.join(project_root_path, 'uploads')

    # 接口白名单
    WHITE_PAI_LIST = [
        'api.register',
        'api.logout',
        'api.login',
        'api.index',
        'api.gettokenbyaccount',
        'api.authenticate',
        # 'api.downloadimage',
        'static',
    ]

    # 邮件配置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('admin', MAIL_USERNAME)
    MAIL_TOKEN = "benny-mail-password"  # 用于验证发送邮件的请求是否来源安全

    # 阿里云短信业务配置信息
    SMS_ACCESS_KEY_ID = "128548974",  # key ID
    SMS_ACCESS_KEY_SECRET = "323232",  # 密钥
    SMS_SIGN_NAME = "设置签名",  # 签名
    AUTHENTICATION = "SMS_1551323",  # 身份验证模板编码
    LOGIN_CONFIRMATION = "SMS_155546",  # 登陆确认模板编码
    LOGIN_EXCEPTION = "SMS_1556546",  # 登陆异常模板编码
    USER_REGISTRATION = "SMS_1551654625",  # 用户注册模板编码
    CHANGE_PASSWORD = "SMS_155126456",  # 修改密码模板编码
    INFORMATION_CHANGE = "SMS_1551265463",  # 信息修改模板编码
