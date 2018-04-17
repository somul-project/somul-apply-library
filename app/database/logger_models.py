from app.database import db, TimestampMixin


class LOGTYPE:
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"


class Log(db.Model, TimestampMixin):
    _id = db.Column('id', db.Integer, primary_key=True,
                    autoincrement=True)

    logtype = db.Column(db.String(20), nullable=False, default="")
    content = db.Column(db.JSON, nullable=False, default="")

    def __repr__(self):
        return '<%r %r %d>' % (self.__class__.__name__,
                               self.log_type, self._id)
