from flask_restful import Resource, reqparse

from webAPi.constant import ReqJson
from webAPi.extensions import db
from webAPi.extensions import jwt_manager
from webAPi.models.user import User
from webAPi.utils.com import setSHA256


class Register(Resource):

    def post(self):
        """register"""
        req = ReqJson()
        parse = reqparse.RequestParser(bundle_errors=False)
        parse.add_argument('app_id', type=str, required=False, help='请输入应用id', location='form')
        parse.add_argument('account', type=str, required=False, help='请输入账号信息', location='form')
        parse.add_argument('password', type=str, required=False, help='请输入密码', location='form')
        front_data = parse.parse_args()

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
        req = ReqJson()  # 预设登录失败的情况， 缩减代码量
        parse = reqparse.RequestParser()
        # TODO required=True, 会自动抛出异常，但返回接口格式不标准，弃用
        parse.add_argument('app_id', type=str, required=False, help='请输入应用id', location='form')
        parse.add_argument('account', type=str, required=False, help='请输入账号信息', location='form')
        parse.add_argument('password', type=str, required=False, help='请输入密码', location='form')
        front_data = parse.parse_args()

        user = User.query.filter_by(account=front_data.get('account')).filter_by(
            app_id=front_data.get('app_id')).first()
        if front_data['app_id'] is None:
            req.msg = "请输入应用id"
        elif not front_data.get('account'):
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
            access_token = jwt_manager.encode_token(front_data['account'], fresh=True)
            # TODO 设置刷新token 的使用策略
            refresh_token = jwt_manager.encode_fresh_token(front_data['account'])

            req.code = 0
            req.data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
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
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('app_id', type=str, required=False, help='请输入应用id', location='form')
        # 自定义token解析
        # parse.add_argument('Authorization', type=str, help='请携带token', location=['headers', 'args'])
        front_data = parse.parse_args()

        token_info = jwt_manager.verify_jwt()
        account = token_info['identity']
        user = User.query.filter_by(app_id=front_data.get('app_id')).filter_by(account=account).first()

        if front_data['app_id'] is None:
            req.msg = "请输入应用id"
        elif user is None:
            req.msg = "账号不存在"
        else:
            req.code = 0
            req.data = {
                "id": user.id,
                "app_id": user.app_id,
                "account": user.account,
                "status": user.status,
                "created_at": user.create_time_str
            }
            req.msg = "token验证通过"
        return req.result


class ChangePassword(Resource):
    def post(self):
        """change password"""
        req = ReqJson(msg="修改密码成功")
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('password', type=str, required=True, help='请输入新密码', location='form')
        parse.add_argument('confirm', type=str, required=True, help='请确认新密码', location='form')
        parse.add_argument('app_id', type=str, required=True, help='请输入应用id', location='form')
        front_data = parse.parse_args()
        req.data = front_data
        return req.result


class RefreshToken(Resource):
    def post(self):
        """refresh token"""


class Logout(Resource):
    def get(self):
        """logout"""
        req = ReqJson()
        parse = reqparse.RequestParser(bundle_errors=True)
        parse.add_argument('Authorization', type=str, help='请携带token', location=['headers', 'args'])
        front_data = parse.parse_args()
        req.data = front_data
        return req
