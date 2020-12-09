# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import json
from flask import g
from flask import request
from flask_restful import reqparse
from flask_restful import Resource
from webAPi.constant import ReqJson
from webAPi.models.cron import Cron
from webAPi.extensions import db
from webAPi.extensions import cron_scheduler

cron_setting_parse = reqparse.RequestParser()
# TODO required=True, 会自动抛出异常，但返回接口格式不标准，弃用
cron_setting_parse.add_argument('id', type=str, location='json')
cron_setting_parse.add_argument('cron', type=dict, location='json')
cron_setting_parse.add_argument('callback_url', type=str, location='json')
cron_setting_parse.add_argument('loop', type=int, location='json')
cron_setting_parse.add_argument('description', type=str, location='json')


class CronTask(Resource):

    def get(self):
        """crontab tasks"""
        req = ReqJson()
        app_id = g.app_id
        crontabs = Cron.query.filter_by(app_id=app_id).all()
        if not crontabs:
            req.code = 0
            req.data = []
        else:
            data = []
            for cron in crontabs:
                data.append(dict(id=cron.id,
                                 crontab=cron.crontab,
                                 callback_url=cron.callback_url,
                                 next_run_date=cron.next_run_date,
                                 loop=cron.loop,
                                 status=cron.status,
                                 description=cron.description,
                                 try_count=cron.try_count,
                                 update_at=cron.update_time_str))
            req.code = 0
            req.data = data
        # print(cron_scheduler.scheduler.print_jobs())
        return req.result

    def post(self):
        """add task"""
        req = ReqJson()
        app_id = g.app_id
        front_data = cron_setting_parse.parse_args()
        cron = front_data.get("cron")
        callback_url = front_data.get("callback_url")
        loop = front_data.get("loop")
        description = front_data.get("description")

        app_id = g.app_id
        if not cron:
            req.msg = "请输入任务时间配置"
        elif not callback_url:
            req.msg = "请输入回调链接"
        elif loop not in [0, 1]:
            req.msg = "参数取值超出范围"
        else:
            cron_str = json.dumps(cron, ensure_ascii=False)
            cron = Cron(app_id=app_id, crontab=cron_str, callback_url=callback_url,
                        loop=loop, description=description)
            # 实现apscheduler任务添加
            front_data['job_id'] = cron.id
            cron_scheduler.add_task(front_data)
            req.code = 0
            db.session.add(cron)
            db.session.commit()
        return req.result

    def put(self):
        """update task"""
        req = ReqJson()
        front_data = cron_setting_parse.parse_args()
        _id = front_data.get("id")
        cron = front_data.get("cron")
        callback_url = front_data.get("callback_url")
        loop = front_data.get("loop")
        description = front_data.get("description")

        app_id = g.app_id
        target_cron = Cron.query.filter_by(app_id=app_id). \
            filter_by(id=_id).first()
        if not target_cron:
            req.msg = "对象不存在"
            return req.result
        if cron:
            cron_str = json.dumps(cron, ensure_ascii=False)
            target_cron.crontab = cron_str
        if callback_url:
            target_cron.callback_url = callback_url
        if loop:
            target_cron.loop = loop
        if description:
            target_cron.description = description
        # 删除旧的任务，重新启动
        cron_scheduler.delete_task(job_id=_id)
        cron_scheduler.add_task(target_cron.get_params())
        req.code = 0
        db.session.add(target_cron)
        db.session.commit()
        return req.result

    def delete(self):
        """delete task"""
        req = ReqJson()
        _id = request.args.get('id')

        app_id = g.app_id
        crontab = Cron.query.filter_by(app_id=app_id). \
            filter_by(id=_id).first()
        if not crontab:
            req.msg = "对象不存在"
        else:
            req.code = 0
            db.session.delete(crontab)
            db.session.commit()
            cron_scheduler.delete_task(job_id=_id)
        return req.result
