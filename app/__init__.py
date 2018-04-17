from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.database import db
from app.utils.hooks import add_before_and_after_hook, add_request_hook


def create_app(config):
    _app = Flask(__name__)
    _app.config.from_object(config)
    _app.secret_key = config.secret_key
    CORS(_app, resources={r"/*": {"origins": "*"}})

    from app.views.library import library
    from app.views.admin import admin
    from app.views.verify import verify
    from app.views.volunteer import volunteer
    from app.views.home import home
    _app.register_blueprint(home, url_prefix="/")
    _app.register_blueprint(library, url_prefix="/library")
    _app.register_blueprint(admin, url_prefix="/admin")
    _app.register_blueprint(verify, url_prefix="/verify")
    _app.register_blueprint(volunteer, url_prefix="/volunteer")

    from app.v1.controllers.libraries import libraries_api
    from app.v1.controllers.maps import maps_api
    from app.v1.controllers.users import users_api
    from app.v1.controllers.admin import admin_api
    from app.v1.controllers.signin import signin_api
    from app.v1.controllers.logger import logger_api

    _app.register_blueprint(libraries_api, url_prefix='/api/v1/library')
    _app.register_blueprint(maps_api, url_prefix='/api/v1/map')
    _app.register_blueprint(users_api, url_prefix='/api/v1/user')
    _app.register_blueprint(admin_api, url_prefix="/api/v1/admin")
    _app.register_blueprint(signin_api, url_prefix='/api/v1/signin')
    _app.register_blueprint(logger_api, url_prefix='/api/v1/logger')
    add_request_hook(libraries_api)
    add_request_hook(maps_api)
    add_request_hook(users_api)
    add_request_hook(admin_api)
    add_request_hook(signin_api)

    db.init_app(_app)
    Migrate(_app, db)
    add_before_and_after_hook(_app)

    return _app
