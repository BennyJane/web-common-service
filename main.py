# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from webAPi import create_app

# 用于部署启动项目:
app = create_app()
config = app.config

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.get("HOST", 5000))
