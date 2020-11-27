from celery.utils.log import get_logger

from webAPi.tasks import celery_app

logger = get_logger(__name__)


@celery_app.task
def week(id):
    """每周执行的任务"""
    print("running week task...")
