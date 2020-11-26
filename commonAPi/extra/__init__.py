from flask import Blueprint
from flask_restful import Api

extra_bp = Blueprint('extra', __name__)
extra_api = Api(extra_bp)
