# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/20 23:14
# Warning    ：The Hard Way Is Easier


workers = 2
threads = 4
bind = "0.0.0.0:8020"
worker_connections = 2000
pidfile = "gunicorn.pid"
accesslog = "./logs/gunicorn/gunicorn_access.log"
errorlog = "./logs/gunicorn/gunicorn_error.log"
loglevel = "debug"
reload = True
