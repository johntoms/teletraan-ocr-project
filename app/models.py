from app import db
from app.utils.toolkit import create_id


class OCRLogging(db.Model):
    """图片识别记录"""
    __tablename__ = 'ocr_logging'
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    id = db.Column(db.String(64), default=create_id, unique=True)
    image_file_name = db.Column(db.String(256), default='non-filename.jpg')
    ocr_result = db.Column(db.String(256))

    def __repr__(self):
        return '<OCRLogging %s>' % self.image_file_name

    def from_dict(self, data):

        for column in self.__table__.columns:
            if column.name in 'seq':
                continue
            setattr(self, column.name,
                    data.get(column.name, getattr(self, column.name)))
        db.session.add(self)
        db.session.commit()
