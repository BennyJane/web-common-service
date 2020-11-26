from flask_restful import Resource


class Login(Resource):
    def get(self):
        """login"""
        return "hello world"

    def post(self):
        """login"""


class Logout(Resource):
    def get(self):
        """logout"""


class Register(Resource):
    def get(self):
        """register"""

    def post(self):
        """register"""
