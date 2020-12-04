# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

from celery.utils.log import get_logger

from webAPi.tasks import celery_app

logger = get_logger(__name__)


@celery_app.task
def week(id):
    """每周执行的任务"""
    print("running week task...")
