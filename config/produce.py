import os
from .base import BaseConfig, prefix, project_root_path


class ProduceConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(project_root_path, 'data-produce.db')

    # 添加celery配置
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    imports = ('proStruct.services.tasks')
