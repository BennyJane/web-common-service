from flask_restful import Resource, reqparse

from webAPi.constant import ReqJson
from webAPi.extensions import db
from webAPi.models.user import User


class Login(Resource):
    def post(self):
        """login"""
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('app_id', type=str, required=True, help='请输入应用id', location='form')
        parse.add_argument('account', type=str, required=True, help='请输入账号信息', location='form')
        parse.add_argument('password', type=str, required=True, help='请输入密码', location='form')
        front_data = parse.parse_args()

        req = ReqJson(msg="登录成功", data=front_data)
        return req.result


class Logout(Resource):
    def get(self):
        """logout"""


class Register(Resource):

    def post(self):
        """register"""
        req = ReqJson(msg="注册成功")
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('app_id', type=str, required=True, help='请输入应用id', location='form')
        parse.add_argument('account', type=str, required=True, help='请输入账号信息', location='form')
        parse.add_argument('password', type=str, required=True, help='请输入密码', location='form')
        front_data = parse.parse_args()

        user = User.query.filter_by(account=front_data['account']).first()
        if user:
            req.code = 1
            req.msg = '账号已存在'
        user = User(account=front_data['account'], app_id=front_data['app_id'])
        db.session.add(user)
        db.session.commit()
        return req.result
