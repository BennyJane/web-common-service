from flask import redirect, url_for, g, current_app, request
from webAPi.models.user import User
from webAPi.extensions import jwt_manager, redis_conn
from webAPi.constant import ReqJson


def register_before_after(app):
    app.before_request(login_require)
    pass

# 视图窗口验证
def login_require():
    req = ReqJson()
    # TODO 跳过白名单，修改为装饰器
    config = current_app.config
    white_api_list = config.get("WHITE_PAI_LIST")
    view_endpoint = request.endpoint
    print(view_endpoint)
    if view_endpoint in white_api_list:
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



def whiteApi(blueprint_name:str):
    white_apis = []

    def wrapper(f):




