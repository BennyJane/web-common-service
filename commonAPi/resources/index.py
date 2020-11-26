from flask_restful import Resource

from commonAPi.constant import ReqJson


class Index(Resource):
    def get(self):
        req = ReqJson(msg="Welcome here! This is a project to relize common functions in the development fo web.")
        return req.result
