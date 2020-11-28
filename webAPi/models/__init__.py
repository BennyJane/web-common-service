from datetime import datetime

from webAPi.extensions import db

Column = db.Column


class BaseMixin(object):  # 参考superset项目
    create_at = Column(db.DateTime, default=datetime.utcnow)
    update_at = Column(db.DateTime, default=datetime.utcnow)


from .user import User
from .appInfo import AppInfo
