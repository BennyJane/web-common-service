from flask_restful import Resource, reqparse

from webAPi.constant import ReqJson


class LocalUploadFile(Resource):
    def post(self):
        """local upload"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument("tag", type=str, location='form')
        parse.add_argument("conf_type", type=str, location='form')
        parse.add_argument("file", type=str, location='form')

        return req.result


class GetImage(Resource):
    def get(self):
        """get image"""


class DownloadImage(Resource):
    def post(self):
        """download image"""
