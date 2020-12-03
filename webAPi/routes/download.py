import os
import json
from flask import g
from flask import request
from webAPi.extensions import db
from flask import send_from_directory
from flask_restful import Resource
from flask_restful import reqparse
from webAPi.constant import ReqJson
from webAPi.utils.decorator import WhiteApi
from webAPi.utils.load_libs import SimpleUpload
from webAPi.models.appInfo import AppInfo


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


@WhiteApi("api")
class DownloadImage(Resource):
    # method_decorators = [WhiteApi("api_bp")]

    @staticmethod
    def downingAndPreview(as_attachment=True):  # 减少重复代码
        req = ReqJson()
        parse = reqparse.RequestParser()
        parse.add_argument('filename', type=str, location='args')  # 上传文件类型
        parse.add_argument('tag', type=str, location='args')  # 上传文件类型
        front_data = parse.parse_args()
        filename = front_data.get("filename")
        tag = front_data.get("tag")

        def get_file_path():  # 借助闭包，解决逻辑顺序的
            upload_path = SimpleUpload.upload_path(tag)
            target_file: str = os.path.join(upload_path, filename)
            yield from [target_file, target_file, upload_path]

        file_gen = get_file_path()  # 只是返回生成器对象，函数内部并没有执行
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
            send_from_directory(upload_dir_path, filename, as_attachment=as_attachment)
            return send_from_directory(upload_dir_path, filename, as_attachment=as_attachment)
        return req

    def get(self):
        """download image"""
        req = DownloadImage.downingAndPreview()
        return req.result


@WhiteApi("api")  # 生产环境需要注释该装饰器，并修改SimpleUpload.upload_path中内容
class GetImage(Resource):
    def get(self):
        """get image: 预览接口"""
        req = DownloadImage.downingAndPreview(as_attachment=False)
        if isinstance(req, ReqJson):
            return req.result
        return req


class UpdateFileConf(Resource):

    def get(self):
        """获取数据库中项目上传文件相关的配置"""
        req = ReqJson()
        req.code = 0
        req.data = AppInfo.get_app_info().upload_conf
        return req.result

    def post(self):
        """修改项目上传文件相关配置"""
        req = ReqJson()
        parse = reqparse.RequestParser()
        # postman 中从 raw-json 中发送信息，从form中无法获取信息
        # FIXME 注意解析内容为 dict 还是 list
        parse.add_argument('update_conf', type=dict, location='json')  # 上传文件配置信息，json格式信息
        front_data = parse.parse_args()
        update_conf = front_data.get("update_conf")

        app_info = AppInfo.get_app_info()
        ori_app_conf = app_info.upload_conf

        if not update_conf:
            req.msg = "请上传需要更新的配置信息"
        else:
            try:
                ori_app_conf.update(update_conf)
            except Exception as e:
                raise Exception(f"配置信息更新失败: {str(e)}")
            else:
                app_info.conf = json.dumps(ori_app_conf, ensure_ascii=True)
                req.code = 0
                req.msg = "更新成功"
                req.data = ori_app_conf
                db.session.commit()
        return req.result
