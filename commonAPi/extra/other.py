from flask_restful import Resource

from commonAPi.constant import ReqJson


class Other(Resource):
    def get(self):
        return ReqJson(msg="other_api").result
