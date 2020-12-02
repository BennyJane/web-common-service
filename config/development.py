import os

from .base import BaseConfig, prefix, project_root_path


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(project_root_path, 'data-dev.db')

    # 添加celery配置
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    imports = ('proStruct.services.tasks')

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    # 测试账号
    TEST_APP_ID = 'dc601e113be8a2e622f9f9a3f363eb93'
    TEST_ACCOUNT = '15845623256'
    TEST_PASSWORD = '8b18762706f0c6854d967b6bb36a97df318654f44b9fe007078149759f25f9d2'  # aaasss123
