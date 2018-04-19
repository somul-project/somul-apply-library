from flask import render_template, Blueprint

from app.database.models import SpeakerInfo
from app.v1.controllers.logger import LoggerResource

admin = Blueprint('views.admin', __name__)


@admin.route("/")
def index():
    speakers = SpeakerInfo.query.filter_by(admin_approved=None)
    return render_template("admin/admin_matching.html", speakers=list(speakers))


@admin.route("/log")
def log():
    results = LoggerResource().get()
    return render_template("admin/admin_log.html", logs=list(results))
