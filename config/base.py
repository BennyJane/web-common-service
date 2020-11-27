import os
from _compat import win

project_root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

prefix = 'sqlite:////'  # linux 下前缀
if win:
    prefix = 'sqlite:///'


class BaseConfig:
    PROJECT_NAME = "web-common-service"
    PROJECT_ROOT_PATH = project_root_path

    SESSION_KEY = 'BENNY JANE'
    IS_DEBUG = True

    SQLITE_PREFIX = prefix
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX + ':memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
