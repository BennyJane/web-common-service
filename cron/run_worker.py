import os
import sys
from celery import Celery

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

from webAPi.tasks import celery_app

# import necessary tasks

import webAPi.tasks.periods

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        celery_app.start(argv=['tasks', 'worker', '-P', 'eventlet', '-E', '-l', 'INFO'])
    else:
        celery_app.start(argv=['tasks', 'worker', '-E', '-l', 'INFO'])
