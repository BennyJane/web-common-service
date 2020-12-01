from webAPi.models import db, Column, BaseMixin
from webAPi.utils.com import produce_id


class Downloading(db.Model, BaseMixin):
    __tablename__ = 'downloading'
    id = Column(db.String(32), primary_key=True)
    app_id = Column(db.String(32), nullable=False, comment="不同应用的标识id")
    name = Column(db.String(120), nullable=False, comment="文件原始名称")
    file_type = Column(db.String(120), nullable=False, comment="上传文件的类型")

    def __init__(self, *args, **kwargs):
        # 设置id的默认值
        if kwargs.get('id') is None:
            kwargs['id'] = produce_id()
        super().__init__(*args, **kwargs)
