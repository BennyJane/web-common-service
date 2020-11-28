# -*- coding: utf-8 -*-
# @Time : 2020/10/21
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
import datetime
import functools
import uuid

import jwt
from flask import request, jsonify

"""
token加密主要通过jwt包来完成，
- token的刷新，通过一个专门的接口实现，当access_token 失效后，会利用fresh_token来获取新的token，
同时将 jwt中字段fresh修改为false，将当前token标记为非新鲜token。
    - fresh_token 由前端存储？？
- 需要一个装饰器，用来限制一些安全级别较高的端口，必须使用未刷新过的token，也就是新鲜token才能访问
- 

bug:
jwt不支持 sha256算法
"""


# 异常处理
class JWTException(Exception):
    """jwt异常处理基类"""


class JWTDecodeError(JWTException):
    """jwt 解码异常"""


class InvalidHeaderError(JWTException):
    """jwt 请求头设置异常"""


class JWTManager(object):
    def __init__(self, secret=None, expire_date=1, fresh_expire_date=7, algorithm="HS256"):
        if not secret:
            secret = "skdfsahuisksdfkl"
        self.secret = secret  # 用于JWT编码的盐
        self.token_expire = datetime.timedelta(minutes=expire_date)
        self.fresh_expire = datetime.timedelta(days=fresh_expire_date)
        self.algorithm = algorithm
        self.auth_header = "Authorization"
        self.token_prefix = "Bearer"

    def init_app(self, app):
        """从flask实例的配置文件中读取配置"""
        config = app.config
        self.secret = config.get('SESSION_KEY')

    def encode_token(self, identity, fresh):
        res = _encode_token(identity, self.token_expire, self.secret, self.algorithm, fresh)
        return res

    def encode_fresh_token(self, identity):
        res = _encode_fresh_token(identity, self.fresh_expire, self.secret, self.algorithm)
        return res

    def decode_jwt(self, token):
        _decode_jwt(token, self.secret, self.algorithm)

    def verify_jwt(self):
        res = _verify_jwt(self.auth_header, self.token_prefix, self.secret, self.algorithm)
        return res

    @staticmethod
    def jwt_required(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                jwt_data = _verify_jwt()
            except Exception as e:
                return jsonify({'msg': f"{str(e)}"}), 422
            if jwt_data['type'] != 'access':
                return jsonify({'msg': '只有access token可以访问该端口'}), 401
            return f(*args, **kwargs)

        return wrapper


"""
- 定义为单独的函数，允许其被单独使用
"""


def _encode_token(identity, expire, secret, algorithm, fresh):
    """
    :param identity:  用户ID，用于区别不同用户
    :param expire:  过期时间
    :param secret:  加密盐
    :param algorithm: 加密算法
    :param fresh:  是否为新鲜的token
    :return: 编码后的JWT
    """
    # FIXME 使用 datetime.datetime.now() 会报错，会报 The token is not yet valid (nbf)
    now = datetime.datetime.utcnow()
    token_data = {
        "exp": now + expire,  # exp token过期时间
        # token的开始生效时间，当前时间在开始时间之前，抛出错误 jwt.exceptions.InvalidIssuedAtError: Issued At claim (iat) cannot be in the future
        "iat": now,
        # token的生效时间， 如果在没有到达生效时间的时候，使用，报错 jwt.exceptions.ImmatureSignatureError: The token is not yet valid (nbf)
        # 可以不设置
        "nbf": now,
        "jti": str(uuid.uuid4()),
        "identity": identity,
        "fresh": fresh,  # bool， 登录，修改密码时，设置为true；刷新token后，设置为false
        # 区别不同的应用场景
        "type": "access"
    }
    bytes_str = jwt.encode(token_data, secret, algorithm)
    return bytes_str.decode('utf-8')


def _decode_jwt(token, secret, algorithm):
    try:
        res = jwt.decode(token, secret, algorithm)
        print('decode', res)
        return res
    except jwt.ExpiredSignatureError:
        raise JWTDecodeError("token失效")
    except jwt.InvalidTokenError:
        raise InvalidHeaderError("token无效")
    except Exception as e:
        raise e
    # except jwt.InvalidTokenError:
    #     # todo 区别具体原因
    #     raise Exception("token 验证错误")


def _encode_fresh_token(identity, fresh_expire, secret, algorithm):
    now = datetime.datetime.utcnow()
    token_data = {
        'exp': now + fresh_expire,
        'iat': now,
        # 'nbf': now,
        'jti': str(uuid.uuid4()),
        'identity': identity,
        'type': 'refresh',
    }
    bytes_str = jwt.encode(token_data, secret, algorithm)
    return bytes_str.decode("utf-8")


def _verify_jwt(auth_header, token_prefix, secret, algorithm):
    """验证request请求中包含的token"""
    auth_header = request.headers.get(auth_header, None)
    if not auth_header:
        raise JWTDecodeError("token请求参数不正确")
    parts = auth_header.split()
    if parts[0] != token_prefix:
        msg = "格式错误，应该为 'Bearer <JWT>'"
        raise InvalidHeaderError(msg)
    elif len(parts) != 2:
        msg = "格式错误，应该为 'Bearer <JWT>'"
        raise InvalidHeaderError(msg)
    token = parts[1]
    return _decode_jwt(token, secret, algorithm)
