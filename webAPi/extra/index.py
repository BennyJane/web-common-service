from flask_restful import Resource

from webAPi.constant import ReqJson


class Index(Resource):
    def get(self):
        req = ReqJson(code=0,
                      data={
                          "project": "公共项目",
                          "brief": "该项目独立实现了用户、文件存储、邮件、定时任务等功能模块。"
                      },
                      msg="Welcome here! This is a project to relize common functions in the development fo web.")

        return req.result
