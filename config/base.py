import os
from _compat import win, modifyPath

project_root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

prefix = 'sqlite:////'  # linux 下前缀
if win:
    prefix = 'sqlite:///'


class BaseConfig:
    PROJECT_NAME = "web-common-service"
    PROJECT_ROOT_PATH = project_root_path
    HOST = 8002

    SESSION_KEY = 'BENNY JANE'
    IS_DEBUG = True

    SQLITE_PREFIX = prefix
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX + ':memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # 支持上传的文件类型
    UPLOAD_TYPE = ('image', 'doc', 'video')
    UPLOAD_ALLOW_TYPE = {
        "image": ("png", 'jpg', 'gif', 'webp'),
        "doc": ('doc', 'docx', 'pdf', 'csv', 'xls'),
        "video": (),
    }

    UPLOAD_PATH = os.path.join(project_root_path, 'uploads')

    # 接口白名单
    WHITE_PAI_LIST = [
        'api.register',
        'api.logout',
        'api.login',
        'api.index',
        'api.gettokenbyaccount',
        'api.authenticate',
        # 'api.downloadimage',
        'static',
        'index',
    ]
