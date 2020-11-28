from flask_restful import Api


def register_extra_api(app):
    extra_api = Api(app)
    # extra_api.init_app(app)  # 这样的定义方式不起作用
    from .index import Index
    extra_api.add_resource(Index, '/')
