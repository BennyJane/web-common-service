# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import datetime
from sqlalchemy import and_
from flask_restful import reqparse
from flask_restful import Resource

from webAPi.response import ReqJson
from webAPi.models.user import User
from webAPi.utils.com import setSHA256
from webAPi.utils.com import CaptchaTool
from webAPi.utils.com import produce_id
from webAPi.extensions import db
from webAPi.extensions import redis_conn
from webAPi.extensions import jwt_manager
from webAPi.utils.decorator import WhiteApi

login_register_parse = reqparse.RequestParser()
# required=True, 会自动抛出异常，但返回接口格式不标准，必须重写返回返回方法， 已经解决
login_register_parse.add_argument('app_id', type=str, location='json')
login_register_parse.add_argument('account', type=str, location='json')
login_register_parse.add_argument('password', type=str, location='json')


class Register(Resource):

    def post(self):
        """register"""
        req = ReqJson()
        front_data = login_register_parse.parse_args()
        # FIXME 传入的密码应该使用sha256加密， 前端加密，后端不需要加密 --》 测试设置
        front_data['password'] = setSHA256(front_data.get('password'))
        user = User.query.filter_by(account=front_data.get('account')).first()
        if not front_data.get('app_id'):
            req.msg = '请输入应用id'
        elif not front_data.get('account'):
            req.msg = '请输入账号信息'
        elif not front_data.get('password'):
            req.msg = '请输入密码'
        elif user is not None:
            req.msg = '账号已存在'
        else:
            req.code = 0
            req.msg = '账号创建成功'
            user = User(account=front_data['account'], app_id=front_data['app_id'], password=front_data['password'])
            db.session.add(user)
            db.session.commit()
        return req.result


class Login(Resource):
    def post(self):
        """login"""
        req = ReqJson()  # 预设失败的情况， 缩减代码量
        front_data = login_register_parse.parse_args()
        account = front_data.get('account')
        app_id = front_data.get('app_id')

        user = User.query.filter(and_(User.account == account, User.app_id == app_id)).first()
        if front_data['app_id'] is None:
            req.msg = "请输入应用id"
        elif not account:
            req.msg = "请输入账号信息"
        elif not front_data.get('password'):
            req.msg = "请输入密码"
        elif user is None:
            req.msg = "账号不存在"
        elif user.password != front_data['password']:
            req.msg = "密码错误"
        elif user.status == 1:
            req.msg = "账号被禁用"
        elif user.password == front_data['password']:
            now_time = datetime.datetime.utcnow()  # 这里必须使用utcnow 时间， 不能使用now
            # 生成两个token
            access_token = jwt_manager.encode_token(account, app_id, fresh=True, now=now_time)
            refresh_token = jwt_manager.encode_fresh_token(account, app_id, now=now_time)
            # 将刷新token添加到redis中
            redis_conn.set_refresh_token(account=account, token=refresh_token)
            req.code = 0
            req.data = {
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "app_id": user.app_id,
                    "account": user.account,
                    "status": user.status,
                    # json 中包含时间格式数据，会报错
                    "create_at": user.create_time_str
                }
            }
        return req.result


class Authenticate(Resource):
    def post(self):
        """authenticate"""
        req = ReqJson()
        # 自定义token解析
        token_info, need_update_token = jwt_manager.verify_jwt(redis_conn=redis_conn)
        account = token_info['identity']
        app_id = token_info['appId']
        new_token = ""  # 新token
        if need_update_token:
            now_time = datetime.datetime.utcnow()
            new_token = jwt_manager.encode_token(account, app_id, fresh=False, now=now_time)
        user = User.query.filter_by(app_id=app_id).filter_by(account=account).first()

        if app_id is None:
            req.msg = "请输入应用id"
        elif user is None:
            req.msg = "账号不存在"
        else:
            req.code = 0
            req.msg = "token验证通过"
            req.data = {
                "id": user.id,
                "app_id": user.app_id,
                "account": user.account,
                "status": user.status,
                "created_at": user.create_time_str,
                "update_token": new_token
            }
        return req.result


class GetTokenByAccount(Resource):
    def get(self):
        """get token by account"""
        req = ReqJson()
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('account', type=str, location='args')
        parse.add_argument('app_id', type=str, location='args')
        front_data = parse.parse_args()
        account = front_data.get("account")
        app_id = front_data.get("app_id")

        user = User.query.filter(and_(User.account == account, User.app_id == app_id)).first()

        if account is None:
            req.msg = "请输入账号信息"
        elif app_id is None:
            req.msg = "请输入应用id"
        elif user is None:
            req.msg = "该账号不存在"
        elif user.status is None:
            req.msg = "该账号已被禁用"
        else:
            req.code = 0

            now_time = datetime.datetime.utcnow()  # 这里必须使用utcnow 时间， 不能使用now
            access_token = jwt_manager.encode_token(account, fresh=True, now=now_time)
            refresh_token = jwt_manager.encode_fresh_token(account, now=now_time)
            redis_conn.set_refresh_token(account=account, token=refresh_token)

            req.data = {
                "token": access_token,
                "user": {
                    "id": user.id,
                    "app_id": user.app_id,
                    "account": user.account,
                    "status": user.status,
                    "create_at": user.create_time_str,
                }

            }
        return req.result


class Logout(Resource):
    def get(self):
        """logout"""
        req = ReqJson()
        token_info, need_update_token = jwt_manager.verify_jwt(redis_conn=redis_conn)
        account = token_info.get('identity')
        if account is None:
            req.msg = "请输入账号信息"
        else:
            req.code = 0
            req.msg = "退出登录"
            redis_conn.del_refresh_token(account)
        return req.result


class ChangePassword(Resource):
    def post(self):
        """change password"""
        req = ReqJson()
        parse = reqparse.RequestParser(bundle_errors=False)
        parse.add_argument('password', type=str, location='json')
        parse.add_argument('confirm', type=str, location='json')
        parse.add_argument('app_id', type=str, location='json')
        front_data = parse.parse_args()
        password = front_data.get("password")
        confirm = front_data.get("confirm")
        app_id = front_data.get("app_id")

        token_info, need_update_token = jwt_manager.verify_jwt(redis_conn=redis_conn)
        account = token_info.get("identity")

        user = User.query.filter(and_(User.account == account, User.app_id == app_id)).first()

        if not token_info.get('fresh') or need_update_token:
            req.msg = "请重新验证登录信息(token为刷新token，而不是刚创建的token)"
        elif not password:
            req.msg = "请输入新密码"
        elif not confirm:
            req.msg = "请输入确认密码"
        elif password != confirm:
            req.msg = "两次密码输入不一致"
        elif user is None:
            req.msg = "账号不存在"
        elif password == user.password:
            req.msg = "新密码不能与旧密码一样"
        else:
            req.code = 0
            req.msg = "密码修改成功"
            user.password = password
            db.session.commit()
        return req.result


class AvatarImage(Resource):  # 生成头像存储在本地？ 还是存储在数据库
    def post(self):
        """make avatar"""

    def get(self):
        """get avatar"""


@WhiteApi("api")
class Captcha(Resource):

    def __init__(self):
        self.req = ReqJson()
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('action', required=True, type=str, location='json', help="action字段不为空")
        parse.add_argument('width', type=int, location='json', help="请设置验证码图片宽度")
        parse.add_argument('height', type=int, location='json', help="请设置验证码图片高度")
        parse.add_argument('code', type=str, location='json')
        parse.add_argument('key', type=str, location='json')
        front_data = parse.parse_args()
        self.action = front_data.get("action")
        self.code = front_data.get("code")
        self.key = front_data.get("key")
        self.width = front_data.get("width")
        self.height = front_data.get("height")

    def get(self):
        """get captcha"""
        # target_action = getattr(self, self.action)
        if self.action == 'verify' and hasattr(self, self.action):
            getattr(self, self.action)()  # TODO 需要检测是否可执行
        elif self.action == 'generate' and hasattr(self, self.action):
            getattr(self, self.action)()
        else:
            self.req.msg = "请求方法不存在"

        return self.req.result

    def generate(self):
        if not self.width:
            self.req.msg = "请输入验证码图片宽度"
        elif not self.height:
            self.req.msg = "请输入验证码图片高度"
        else:
            new_captcha = CaptchaTool()
            img, code = new_captcha.get_verify_code(self.width, self.height)
            key = f"captcha:{produce_id()}"
            redis_conn.set(key, code, expire=60 * 3)  # 3分钟过期时间
            self.req.data = {
                "key": key,
                "img": img}

    def verify(self):
        """verify captcha"""

        def get_code_by_redis():
            """使用生成器表达式特性，延迟执行；数据库查询操作只执行了一次"""
            key = redis_conn.get(self.key)
            yield from {key for _ in range(3)}

        gen_key = get_code_by_redis()
        if not self.code:
            self.req.msg = "请输入验证码"
        elif not self.key:
            self.req.msg = "请携带验证码关键字"
        elif not next(gen_key):
            self.req.msg = "请刷新验证码"
        elif next(gen_key) != self.code:
            self.req.msg = "验证码错误"
        elif next(gen_key) == self.code:
            self.req.code = 0
            self.req.msg = "验证通过"
