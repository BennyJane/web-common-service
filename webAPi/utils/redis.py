# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import time
from contextlib import contextmanager

import redis
import datetime
from threading import Thread

from webAPi.log import web_logger
from webAPi.utils.com import request_send_mail
from webAPi.constant import REDIS_REFRESH_TOKEN_KEY
from webAPi.constant import REDIS_MAIL_QUEUE
from webAPi.constant import REDIS_MAIL_INTERVAL


# TODO 实现单例模式，确保redis实例只实例化了一次
class RedisConn:
    def __init__(self, host='127.0.0.1', port=6379, password=''):
        self.host = host
        self.port = port
        self.password = password
        self.conn = None

        # 邮件任务配置项
        self.project_domain = ""

    def init_app(self, app):
        config = app.config
        self.host = config.get('REDIS_HOST')
        self.port = config.get('REDIS_PORT')
        self.password = config.get('REDIS_PASSWORD')
        self.project_domain = config.get("PROJECT_DOMAIN")
        self.cursor()
        # 监听邮件事务处理 ==> 移动到中间件模块中
        Thread(target=self.listen_mail_task, args=[REDIS_MAIL_QUEUE, ], daemon=True).start()

    def cursor(self):
        if self.password:
            pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password)
        else:
            pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.conn = redis.Redis(connection_pool=pool)

    def set(self, key, value, expire=None):
        self.conn.set(key, value, ex=expire)

    def get(self, key):
        return self.conn.get(key)

    def hset(self, key, field, value):
        self.conn.hset(key, field, value)

    def hget(self, key):
        self.conn.hget(key)

    def set_refresh_token(self, account, token, expire=60 * 60 * 24 * 7):
        key = REDIS_REFRESH_TOKEN_KEY.format(account)
        self.conn.set(key, token, ex=expire)  # 过期时间设置为

    def get_refresh_token(self, account):
        res = self.conn.get(REDIS_REFRESH_TOKEN_KEY.format(account))
        return res

    def del_refresh_token(self, account):
        self.conn.delete(REDIS_REFRESH_TOKEN_KEY.format(account))

    """
    ====================================================
    生产/消费者模型
    ====================================================
    """

    def listen_mail_task(self, target_queue):
        while True:
            try:
                time.sleep(REDIS_MAIL_INTERVAL)
                # print("listen task ...", target_queue)
                # blpop: 队列为空, 阻塞； timeout=0, 则无限阻塞
                task_params = self.conn.blpop(target_queue, timeout=0)[1]  # 取出来的数据就是json格式
                # 执行任务
                request_send_mail(task_params, domain=self.project_domain)
            except Exception as e:
                print(e)

    def add_task(self, target_queue, task):
        """向队列中添加数据"""
        self.conn.lpush(target_queue, task)


# 只是保证被锁方法在特定时间段内只执行一次。
@contextmanager
def redis_lock(conn, name, timeout=24 * 60 * 60):
    try:
        today_string = datetime.datetime.now().strftime("%Y-%m-%d")
        key = f"servername.lock.{name}.{today_string}"
        lock = conn.set(key, value=1, nx=True, ex=timeout)
        yield lock  # 新增键会返回True; 键已存在，返回None
    except KeyError as e:  # 捕获未获取锁的异常
        web_logger.info(e)
        return
    except Exception as e:  # 捕获获取锁，但执行过程中报错的情况
        web_logger.debug(e)
    web_logger.info("释放锁 ...")
    conn.delete(key)  # 释放锁，只有获取锁的线程才需要释放锁

    # 这里不能使用 finally来释放锁，导致未获取锁的线程，也可以释放锁
    # finally:
    #     web_logger.info("释放锁 ...")
    #     conn.delete(key)  # 释放锁，只有获取锁的线程才需要释放锁
