from webAPi.models import db, Column, BaseMixin
from webAPi.utils.com import produce_id


class User(db.Model, BaseMixin):
    __tablename__ = 'user'
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    account = Column(db.String(120), nullable=False, comment="用户账号的唯一标识")
    password = Column(db.Text, nullable=False)
    status = Column(db.Integer, default=0, comment="账号状态：0 可用/1 不可用")

    def __init__(self, *args, **kwargs):
        # 设置id的默认值
        if kwargs.get('id') is None:
            kwargs['id'] = produce_id()
        super().__init__(*args, **kwargs)

    @staticmethod
    def insert_test_user():
        test_user = User(id=produce_id(), app_id="dc601e113be8a2e622f9f9a3f363eb93", account="15927166568", password="123456")
        db.session.add(test_user)
        db.session.commit()
