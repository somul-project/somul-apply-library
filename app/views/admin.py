from flask import render_template, Blueprint

from app.database.models import SpeakerInfo

admin = Blueprint('views.admin', __name__)


@admin.route("/")
def index():
    speakers = SpeakerInfo.query.filter_by(SpeakerInfo.admin_approved is None)
    return render_template("admin_matching.html", speakers=speakers)
