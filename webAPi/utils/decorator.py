from flask import g
from flask import request
from flask import current_app
from webAPi.constant import ReqJson
from webAPi.models.user import User
from webAPi.extensions import redis_conn
from webAPi.extensions import jwt_manager


def register_before_after(app):
    app.before_request(login_require)  # 直接使用装饰器函数


# 视图窗口验证
def login_require():
    req = ReqJson()
    # TODO 跳过白名单，修改为装饰器
    config = current_app.config
    white_api_list = config.get("WHITE_PAI_LIST")
    view_endpoint = request.endpoint
    # print(view_endpoint)
    # print(WhiteApi.white_apis)
    if view_endpoint in white_api_list or view_endpoint in WhiteApi.white_apis:
        return None
    # 验证token， 提取信息
    token_info, need_update_token = jwt_manager.verify_jwt(redis_conn=redis_conn)
    account = token_info['identity']
    app_id = token_info['appId']
    if need_update_token:
        req.code = 10001  # 设置特定的code码，前段判断后前往请求刷新token接口
        req.msg = "请刷新token"  #
        # return req.result
        # return redirect(url_for('api.authenticate'))  # 将其重定向到刷新token的接口地址

    user = User.query.filter(User.app_id == app_id).filter(User.account == account).first()
    if user is None:
        raise Exception("账号不存在")
    g.account = user.account
    g.app_id = user.app_id

    return None


"""
更简单的实现方式：
white_apis = [] # 定义全局变量

def white_api(f, blue: str = None):

    endpoint = f"{f.__name__}"
    if blue is not None:
        endpoint = f"{blue}.{f.__name__}"
    white_apis.append(endpoint.lower())
    return f

改进： 在函数上添加属性，实现多次调用之间共享数据

def WhiteApi(f, blue:str=None):
    # 在函数对象中添加属性，作为公共属性使用
    try:
        apis = WhiteApi.white_apis
    except AttributeError:
        WhiteApi.white_apis = []
        
    endpoint = f"{f.__name__}"
    if blue is not None:
        endpoint = f"{blue}.{f.__name__}"
    white_apis.append(endpoint.lower())
    return f

"""


class WhiteApi:
    """使用类实现装饰器：添加免验证的接口白名单"""
    white_apis = []  # 所有类共有的属性, 只在类被创建的时候实例化一次，后续无论该类实例化多少次，都公用该属性

    def __new__(cls, *args, **kwargs):  # 可以不写该方法，允许类被实例化多次，依然可以实现功能
        # 特殊单例用法：只生成一个实例对象，但每次实例化都会重新运行__init__方法
        instance = cls.__dict__.get("__instance__")
        if instance is not None:
            return instance
        cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self, blueprint_name: str = None):
        self.blueprint_name = blueprint_name

    def __call__(self, f):
        endpoint = f"{f.__name__}"
        if self.blueprint_name is not None:
            # FIXME 提防自定义endpoint的试图函数
            endpoint = f"{self.blueprint_name}.{f.__name__}"
        self.white_apis.append(endpoint.lower())
        return f
