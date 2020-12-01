import os
from flask import request, g, send_from_directory, current_app
from flask_restful import Resource, reqparse
from webAPi.constant import ReqJson
from webAPi.utils.load_libs import SimpleUpload


class LocalUploadFile(Resource):
    def post(self):
        """local upload"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument('tag', type=str, location='form')  # 上传文件类型
        # 下面的解析方法没有成功
        # parse.add_argument("pictures", type=werkzeug.datastructures.FileStorage, location='files')
        front_data = parse.parse_args()
        tag = front_data.get('tag')

        simple_upload = SimpleUpload(file=request.files, tag=tag)
        files_info = simple_upload.core()
        req.code = 0
        req.data = {
            "app_id": g.app_id,
            "tag": tag,
            "uploads": files_info,
        }
        req.msg = "上传成功"
        return req.result


class GetImage(Resource):
    def get(self):
        """get image"""


class DownloadImage(Resource):
    def get(self):
        """download image"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument('filename', type=str, location='args')  # 上传文件类型
        parse.add_argument('tag', type=str, location='args')  # 上传文件类型
        front_data = parse.parse_args()
        filename = front_data.get("filename")
        tag = front_data.get("tag")

        def get_file_path():  # 借助闭包，解决逻辑顺序的
            upload_path = SimpleUpload.upload_path(tag)
            target_file = os.path.join(upload_path, filename)
            yield target_file
            yield target_file
            yield upload_path

        file_gen = get_file_path()
        # print(get_file_path())
        print(file_gen)
        if not filename:
            req.msg = "请输入文件名"
        elif not tag:
            req.msg = "请输入文件类型"
        elif not os.path.exists(next(file_gen)):
            req.msg = "文件不存在"
        elif not os.path.isfile(next(file_gen)):  # 非文件类型
            req.msg = "文件不存在)"
        else:
            upload_dir_path = next(file_gen)
            print(f"==================== {upload_dir_path}")
            return send_from_directory(upload_dir_path, filename)
            # return send_from_directory(upload_dir_path, filename, as_attachment=True)

        return req.result
