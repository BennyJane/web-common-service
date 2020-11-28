from flask_restful import Resource

from webAPi.constant import ReqJson


class Index(Resource):
    def get(self):
        req = ReqJson(msg="公共项目接口版本1.0版本")
        return req.result
