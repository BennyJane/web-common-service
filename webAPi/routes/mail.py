from flask_restful import Resource


class MailConf(Resource):
    def get(self):
        """get mail conf"""

    def post(self):
        """add new mail template"""

    def put(self):
        """update mail template"""


class SimpleSendMail(Resource):
    def post(self):
        """send mail to someone"""
