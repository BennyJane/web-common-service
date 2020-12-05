# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import json
from flask import g
from flask import request
from flask import current_app
from sqlalchemy import and_
from flask_restful import Resource
from flask_restful import reqparse

from webAPi.constant import ReqJson
from webAPi.constant import REDIS_MAIL_QUEUE
from webAPi.models.mail import MailTemplate
from webAPi.extensions import db
from webAPi.extensions import redis_conn
from webAPi.utils.decorator import WhiteApi
from webAPi.utils.mail_libs import multi_send_mail


class MailConf(Resource):
    def get(self):
        """get mail conf"""
        req = ReqJson(code=0)
        app_id = g.app_id
        templates = MailTemplate.get_templates(app_id)
        req.data = templates
        return req.result

    def _front_fields(self):
        parse = reqparse.RequestParser()
        parse.add_argument("template_id", type=str, location="json")
        parse.add_argument("alias", type=str, location="json")
        parse.add_argument("subject", type=str, location="json")
        parse.add_argument("template", type=str, location="json")
        front_data = parse.parse_args()
        alias = front_data.get("alias")
        subject = front_data.get("subject")
        template = front_data.get("template")
        template_id = front_data.get("template_id")  # 更新接口使用
        app_id = g.app_id

        return app_id, alias, subject, template, template_id

    def post(self):
        """add new mail template"""
        req = ReqJson()
        app_id, alias, subject, template, _ = self._front_fields()
        mail_existed = MailTemplate.query.filter(
            and_(MailTemplate.app_id == app_id, MailTemplate.subject == subject, MailTemplate.app_id == app_id)).first()
        if not alias:
            req.msg = "请输入邮件模板别名"
        elif not subject:
            req.msg = "请输入邮件模板主题信息"
        elif not template:
            req.msg = "请输入邮件模板样式"
        elif mail_existed:
            req.msg = "该模板已经存在"
        elif not mail_existed:
            req.code = 0
            mail_template = MailTemplate(app_id=app_id, alias=alias, subject=subject, template=template)
            db.session.add(mail_template)
            db.session.commit()
            req.msg = "添加模板"
        return req.result

    def put(self):
        """update mail template"""
        req = ReqJson()
        app_id, alias, subject, template, template_id = self._front_fields()
        mail_template = MailTemplate.query.filter(MailTemplate.id == template_id).filter(
            MailTemplate.app_id == app_id).first()
        if not mail_template:
            req.msg = "该模板不存在"
            return req.result
        if alias:
            mail_template.alias = alias
        if subject:
            mail_template.subject = subject
        if template:
            mail_template.template = template
        db.session.commit()
        req.msg = "更新模板"
        req.code = 0
        return req.result


class AddMail(Resource):
    def post(self):
        """add mail"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument("template_id", type=str, location="json")
        parse.add_argument("alias", type=str, location="json")
        parse.add_argument("to_mail", type=list, location="json")
        parse.add_argument("params", type=dict, location="json")
        front_data = parse.parse_args()
        alias = front_data.get("alias")
        params = front_data.get("params")
        template_id = front_data.get("template_id")
        to_mail = front_data.get("to_mail")

        mail_template = MailTemplate.query.filter(MailTemplate.id == template_id).first()
        if not mail_template:
            req.msg = "模板不存在"
        elif not alias:
            req.msg = "邮件名称不存在"
        elif not to_mail:
            req.msg = "请输入邮件接收者的邮箱"
        else:
            req.code = 0
            req.msg = "邮件稍后会自动发送，请注意查收"

            params = {
                "template_id": template_id,
                "alias": alias,
                "template": mail_template.template,
                "to_mail": to_mail,
                "params": params,
                "mail_token": current_app.config.get("MAIL_TOKEN"),
            }
            # pprint(params)
            mail_params_str = json.dumps(params, ensure_ascii=True)
            redis_conn.add_task(REDIS_MAIL_QUEUE, mail_params_str)
        return req.result


@WhiteApi("api")
class SimpleSendMail(Resource):
    def post(self):
        """send mail by flask-mail"""
        req = ReqJson()

        front_data = request.get_json()
        mail_token = front_data.get("mail_token")
        template_id = front_data.get("template_id")

        target_mail = MailTemplate.query.filter(MailTemplate.id == template_id).first()
        mail_token_back = current_app.config.get("MAIL_TOKEN")

        current_app.logger.info(front_data)

        if mail_token != mail_token_back:
            req.msg = "验证码错误"
        elif not target_mail:
            req.msg = "邮件模板不存在"
        else:
            front_data['template'] = target_mail.template
            multi_send_mail(front_data)
            req.code = 0
            req.msg = "邮件发送成功"
        return req.result
