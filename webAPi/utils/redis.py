# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import redis


from webAPi.constant import REDIS_REFRESH_TOKEN_KEY


class RedisConn:
    def __init__(self, host='127.0.0.1', port=6379, password=''):
        self.host = host
        self.port = port
        self.password = password
        self.conn = None

    def init_app(self, app):
        config = app.config
        self.host = config.get('REDIS_HOST')
        self.host = config.get('REDIS_PORT')
        self.host = config.get('REDIS_PASSWORD')
        self.cursor()

    def cursor(self):
        if self.password:
            pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password)
        else:
            pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.conn = redis.Redis(connection_pool=pool)

    def set_refresh_token(self, account, token, expire=60 * 60 * 24 * 7):
        key = REDIS_REFRESH_TOKEN_KEY.format(account)
        self.conn.set(key, token, ex=expire)  # 过期时间设置为

    def get_refresh_token(self, account):
        res = self.conn.get(REDIS_REFRESH_TOKEN_KEY.format(account))
        return res

    def del_refresh_token(self, account):
        self.conn.delete(REDIS_REFRESH_TOKEN_KEY.format(account))
