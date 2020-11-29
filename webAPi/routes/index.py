from flask_restful import Resource

from webAPi.constant import ReqJson


class Index(Resource):
    def get(self):
        req = ReqJson(
            code=0,
            data={
                "author": "benny jane",
                "version": "0.1.0",
                "create_at": "20201126",
            },
            msg="")
        return req.result
