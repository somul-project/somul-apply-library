from flask import render_template, Blueprint

from app.database.models import SpeakerInfo
from app.v1.controllers.logger import LoggerResource

admin = Blueprint('views.admin', __name__)


@admin.route("/")
def index():
    speakers = SpeakerInfo.query.filter_by(admin_approved=None)
    speaker_list = list()
    for speaker in speakers:
        speaker_list.append({
            "user": {
                "name": speaker.user.name,
                "library_name": speaker.user.library.name,
                "phone": speaker.user.phone,
                "email": speaker.user.email
            },
            "_id": speaker._id,
            "session_time": speaker.session_time,
            "introduce": speaker.introduce.replace("\n", "<br>"),
            "history": speaker.history.replace("\n", "<br>"),
            "title": speaker.title.replace("\n", "<br>"),
            "description": speaker.description.replace("\n", "<br>")
        })
    
    return render_template("admin/admin_matching.html",
                           speakers=speaker_list)


@admin.route("/log")
def log():
    results = LoggerResource().get()
    return render_template("admin/admin_log.html", logs=list(results))
