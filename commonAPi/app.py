from flask import Flask

from commonAPi.extra import extra_bp, extra_api
from commonAPi.extra.other import Other
from commonAPi.resources import api_bp, resources_api
from commonAPi.resources.auth import Login, Logout, Register
from commonAPi.resources.index import Index

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api/v1')  # api必须先绑定蓝图，然后再在flask实例上注册蓝图，顺序不能变
app.register_blueprint(extra_bp, url_prefix='/api/v1/extra')

resources_api.add_resource(Index, '/')
resources_api.add_resource(Login, '/auth/login')
resources_api.add_resource(Logout, '/auth/logout')
resources_api.add_resource(Register, '/auth/register')

# extra
extra_api.add_resource(Other, '/')

if __name__ == '__main__':
    app.run(debug=True)
