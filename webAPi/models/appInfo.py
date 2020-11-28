from collections import namedtuple

from webAPi.extensions import db
from webAPi.models import Column, BaseMixin
from webAPi.utils.com import produce_id

APP_INFO = namedtuple('app_info', 'id name brief status')


class AppInfo(db.Model, BaseMixin):
    __tablename__ = 'app_info'
    id = Column(db.String(32), primary_key=True)
    name = Column(db.String(255), nullable=False, comment="应用名称")
    brief = Column(db.Text, nullable=False, comment="应用简介")
    status = Column(db.Integer, default=0, comment="应用状态：0 可用/1 不可用")

    @staticmethod
    def insert_data():
        app_infos = [
            APP_INFO('dc601e113be8a2e622f9f9a3f363eb93', 'test_project', '这是一个测试项目', 0),
            APP_INFO('1b4925bfa780f5964a2de19e5322dca4', 'school_info', '学校信息网', 0),
        ]
        for info in app_infos:
            app = AppInfo.query.filter_by(name=info.name).first()
            if app is None:
                app_id = info.id if info.id else produce_id()
                app = AppInfo(id=app_id,
                              name=info.name, brief=info.brief, status=info.status)
                db.session.add(app)
            else:  # 更新操作
                app.name = info.name
                app.brief = info.brief
                app.status = info.status
        db.session.commit()
