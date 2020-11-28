from flask import Blueprint
from flask_restful import Api

extra_bp = Blueprint('extra', __name__)
extra_api = Api(extra_bp)


def register_extra_api(app):
    app.register_blueprint(extra_bp)
    from .index import Index

    extra_api.add_resource(Index, '/')
