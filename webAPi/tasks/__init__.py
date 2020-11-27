import os
import sys
import threading
from celery import Celery

from _compat import win

from config import projectConfigs

config_name = os.getenv('FLASK_ENV', 'development')
if config_name not in projectConfigs.keys():
    config_name = 'development'

celery_app = Celery(__name__)
celery_app.config_from_object(projectConfigs[config_name])

# import commonAPi.tasks.periods
#
# if __name__ == '__main__':
#     if win:
#         app.start(argv=['tasks', 'worker', '-P', 'eventlet', '-E', '-l', 'INFO'])
#     else:
#         app.start(argv=['tasks', 'worker', '-E', '-l', 'INFO'])
