from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.database import db
from app.database.models import Library


def create_app(config):
    _app = Flask(__name__)
    _app.config.from_object(config)
    CORS(_app, resources={r"/apply": {"origins": "*"}})

    from app.views import views
    _app.register_blueprint(views)

    from app.v1.controllers.libraries import libraries_api
    from app.v1.controllers.maps import maps_api

    _app.register_blueprint(libraries_api, url_prefix='/api/v1')
    _app.register_blueprint(maps_api, url_prefix='/api/v1')

    db.init_app(_app)
    Migrate(_app, db)

    return _app
