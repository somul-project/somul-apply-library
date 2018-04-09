from app.database import db
from app.utils.errors import DataNotFoundError


def get_or_404(model_clazz, pk):
    instance = db.query(model_clazz).filter_by(_id=pk).first()
    if instance is None:
        raise DataNotFoundError(
            "{} {} Not found".format(model_clazz.__name__, pk))

    return instance
