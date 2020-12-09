# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier

import datetime
import functools
import uuid

import jwt
from flask import request, jsonify

"""
token加密主要通过jwt包来完成，
- token的刷新，通过一个专门的接口实现，当access_token 失效后，会利用fresh_token来获取新的token，
同时将 jwt中字段fresh修改为false，将当前token标记为非新鲜token。
- 需要一个装饰器，用来限制一些安全级别较高的端口，必须使用未刷新过的token，也就是新鲜token才能访问

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
    def __init__(self, secret=None, expire_date=60, fresh_expire_date=7, algorithm="HS256"):
        if not secret:
            secret = "skdfsahuisksdfkl"  # todo 优化该值
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

    def encode_token(self, identity, app_id, fresh, now=None):
        res = _encode_token(identity, app_id, self.token_expire, self.secret, self.algorithm, fresh, now_time=now)
        return res

    def encode_fresh_token(self, identity, app_id, now=None):
        res = _encode_fresh_token(identity, app_id, self.fresh_expire, self.secret, self.algorithm, now_time=now)
        return res

    def decode_jwt(self, token, redis_conn=None):
        res, need_update_token = _decode_jwt(token, self.secret, self.algorithm, redis_conn=redis_conn)
        return res

    def verify_jwt(self, redis_conn=None):
        res, need_update_token = _verify_jwt(self.auth_header, self.token_prefix, self.secret, self.algorithm,
                                             redis_conn=redis_conn)
        return res, need_update_token

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


def _encode_token(identity, app_id, expire, secret, algorithm, fresh, now_time=None):
    """
    :param identity:  用户ID，用于区别不同用户
    :param expire:  过期时间
    :param secret:  加密盐
    :param algorithm: 加密算法
    :param fresh:  是否为新鲜的token
    :param now:  token生成时间
    :return: 编码后的JWT
    """
    # FIXME 使用 datetime.datetime.now() 会报错，会报 The token is not yet valid (nbf)
    now = datetime.datetime.utcnow() if now_time is None else now_time
    token_data = {
        "exp": now + expire,  # exp token过期时间
        # token的开始生效时间，当前时间在开始时间之前，
        # 抛出错误 jwt.exceptions.InvalidIssuedAtError: Issued At claim (iat) cannot be in the future
        "iat": now,
        # token的生效时间， 如果在没有到达生效时间的时候，使用，报错 jwt.exceptions.ImmatureSignatureError: The token is not yet valid (nbf)
        # 可以不设置
        "nbf": now,
        "jti": str(uuid.uuid4()),
        "identity": identity,
        "appId": app_id,
        "fresh": fresh,  # bool， 登录，修改密码时，设置为true；刷新token后，设置为false
        # 区别不同的应用场景
        "type": "access"
    }
    bytes_str = jwt.encode(token_data, secret, algorithm)
    return bytes_str.decode('utf-8')


def _decode_jwt(token, secret, algorithm, redis_conn=None):
    try:
        res = jwt.decode(token, secret, verify=True, algorithms=algorithm)
    except jwt.ExpiredSignatureError:
        return _verify_refresh_token(token, secret, algorithm, redis_conn)
    except jwt.InvalidTokenError:
        raise JWTDecodeError("token无效")
    except Exception as e:
        raise e
    _verify_refresh_token(token, secret, algorithm, redis_conn)  # 不需要改函数的返回值
    return res, False


def _encode_fresh_token(identity, app_id, fresh_expire, secret, algorithm, now_time=None):
    """
    :param identity: 账号ID
    :param fresh_expire: 刷新token的过期时间
    :param secret: 加密参数
    :param algorithm: 加密算法
    :param access_time: access_token 的创建时间， 确保两者创建的时间一致
    :return:
    """
    now = datetime.datetime.utcnow() if now_time is None else now_time
    token_data = {
        'exp': now + fresh_expire,
        'iat': now,
        # 'nbf': now,
        'jti': str(uuid.uuid4()),
        'identity': identity,
        'appId': app_id,
        'type': 'refresh',
    }
    bytes_str = jwt.encode(token_data, secret, algorithm)
    return bytes_str.decode("utf-8")


def _verify_jwt(auth_header, token_prefix, secret, algorithm, redis_conn=None):
    """验证request请求中包含的token"""
    auth_header = request.headers.get(auth_header, None)
    if not auth_header:
        raise JWTDecodeError("没有携带token")
    parts = auth_header.split()
    if parts[0] != token_prefix:
        msg = "格式错误，应该为 'Bearer <JWT>'"
        raise InvalidHeaderError(msg)
    elif len(parts) != 2:
        msg = "格式错误，应该为 'Bearer <JWT>'"
        raise InvalidHeaderError(msg)
    token = str.encode(parts[1], 'utf-8')  # token 需要转化为 bytes类型
    return _decode_jwt(token, secret, algorithm, redis_conn=redis_conn)


def _verify_refresh_token(token, secret, algorithm, redis_conn=None):
    """实现token刷新以及有效性的判断"""
    # 设置 verify=False，直接解析token，不报错
    if not isinstance(token, bytes):
        token = str.encode(token, 'utf-8')
    token_info = jwt.decode(token, secret, verify=False, algorithms=algorithm)
    account = token_info['identity']
    access_token_create_time = token_info['iat']
    refresh_token = redis_conn.get_refresh_token(account=account)
    if refresh_token is None:
        raise JWTDecodeError("刷新token已过期")
    try:
        # 解析refresh_token中的信息
        refresh_token_info = jwt.decode(refresh_token, secret, algorithms=algorithm)
        refresh_token_create_time = refresh_token_info['iat']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise JWTDecodeError("刷新token失效")
    if access_token_create_time < refresh_token_create_time:
        raise JWTDecodeError("旧token失效")
    # 需要重新生成刷新token
    return token_info, True  # 返回token携带的信息，以及是否需要生成新的token
