from flask_sqlalchemy import SQLAlchemy

from app.utils.errors import DataNotFoundError


db = SQLAlchemy()


def get_or_404(model_clazz, pk):
    instance = get_or_none(model_clazz, pk)
    if instance is None:
        raise DataNotFoundError(
            "{} {} Not found".format(model_clazz.__name__, pk))

    return instance


def get_or_none(model_clazz, pk):
    return model_clazz.query.filter_by(_id=pk).first()
