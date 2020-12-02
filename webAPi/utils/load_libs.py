import os
import uuid
from flask import g
from flask import current_app
from _compat import modifyPath
from werkzeug.utils import secure_filename
from webAPi.models.appInfo import AppInfo


class BaseUpload:

    def __init__(self):
        app_id = g.app_id
        app_info = AppInfo.query.get(app_id)
        if not app_info:
            raise Exception("项目不存在")
        self.upload_conf = app_info.upload_conf
        self.upload_types = self.upload_conf.get('allow_file_types')

        self.tag = "image"  # 设置默认值

    @staticmethod
    def upload_path(tag):  # 修改为类方法，以便于在其他地方调用
        """生成项目下特定类型文件存储的目录路径: 该函数只能在flask的请求上线文中运行"""
        # app_id = g.app_id
        app_id = "dc601e113be8a2e622f9f9a3f363eb93"
        config = current_app.config
        upload_path = config.get("UPLOAD_PATH")
        path_prefix = modifyPath("{}\{}".format(app_id, tag))  # 不能以\开头， 否则会报错
        return os.path.join(upload_path, path_prefix)

    @property
    def app_save_path(self):
        app_save_path = SimpleUpload.upload_path(self.tag)
        if not os.path.exists(app_save_path):
            os.makedirs(app_save_path)  # 创建多级目录
            # os.mkdir(app_save_path) # mkdir 创建单级目录，
        return app_save_path

    def rename(self, file):
        """重新命名"""
        filename = file.filename
        try:
            # name, ext = filename.split('.', 1)
            name, ext = os.path.splitext(filename)  # 扩展名带有点号： .
        except IndexError as e:
            raise IndexError("文件名称格式不正确: <filename.ext>")
        except Exception as e:
            raise Exception(str(e))
        if ext.strip('.') not in self.upload_conf[self.tag].get('allow_extensions'):
            raise Exception("文件扩展名不支持")
        filename = secure_filename(filename)
        new_name = str(uuid.uuid1(node=30)) + ext
        return filename, new_name


class SimpleUpload(BaseUpload):

    def __init__(self, file, tag):
        super(SimpleUpload, self).__init__()
        self.files: dict = file
        self.tag = tag

    def check_size(self, filename: str, ori_name: str):
        """检查文件大小"""
        target_file = os.path.join(self.app_save_path, filename)
        file_size = round(os.path.getsize(target_file))
        file_limit_size = self.upload_conf[self.tag].get("max_content_size")
        if file_size > file_limit_size:
            self.remove(filename)
            raise Exception("{} 上传失败: 大小超过{}M，".format(ori_name, (file_limit_size / 1024 / 1024), ))

    def check_type(self):  # TODO 改进文件大小检测的方法
        if self.tag is None or self.tag not in self.upload_types:
            raise Exception("上传文件类型不正确")

    def save(self, filename: str, file):
        """存储"""
        saved_path = os.path.join(self.app_save_path, filename)
        file.save(saved_path)

    def remove(self, filename: str):
        target_file = os.path.join(self.app_save_path, filename)
        if os.path.exists(target_file):
            os.remove(target_file)

    def core(self):
        files_info = []
        self.check_type()
        for file in self.files.values():  # 允许上传多个同类型的文件
            if not file.filename:  # 跳过空文件; TODO 优化检测条件
                continue
            ori_name, new_name = self.rename(file)
            try:
                self.save(new_name, file)
            except Exception as e:
                self.remove(new_name)
                raise Exception(str(e))
            else:
                # TODO 当多个文件中存在文件大小超限制时，其他文件上传成功了 ==> 考虑修改？？
                # 当上传成功后，才需要检查文件大小
                self.check_size(new_name, ori_name)
                # 返回文件信息： 文件新的名称
                files_info.append({
                    "filename": ori_name,
                    "new_name": new_name
                })
        return files_info


if __name__ == '__main__':
    SimpleUpload('dfd', 'dsf')
