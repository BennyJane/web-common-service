# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:25
# Warning    ：The Hard Way Is Easier
from threading import Thread
from flask_mail import Message
from flask import current_app
from webAPi.extensions import mail


def _send_async_mail(app, message):
    """异步发送邮件"""
    with app.app_context():
        mail.send(message=message)


def send_mail(subject, to, template):
    app = current_app._get_current_object()
    if not isinstance(to, list):
        to = [to]
    message = Message(subject, recipients=to, html=template)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def multi_send_mail(mail_info: dict):
    template = mail_info.get("template")
    subject = mail_info.get("alias")
    to_mail = mail_info.get("to_mail")
    template_params = mail_info.get("params")
    mail_template = template.format(**template_params)
    send_mail(subject=subject, to=to_mail, template=mail_template)



