from flask import request, render_template, Blueprint

from app.database.models import SpeakerInfo
from app.v1.controllers.logger import LoggerResource
from app.config import Config

admin = Blueprint('views.admin', __name__)


@admin.route("/")
def index():

    secret = request.args.get('secret')

    # should write secret code
    if secret is None:
        return '', 404

    # wrong secret code
    if secret != Config.secret_auth_code:
        return '', 404

    speakers = SpeakerInfo.query.filter_by(admin_approved=None)
    speaker_list = list()
    for speaker in speakers:
        speaker_list.append({
            "user": {
                "name": speaker.user.name,
                "library_name": speaker.user.library.name,
                "phone": speaker.user.phone,
                "email": speaker.user.email,
                "has_experienced_somul": speaker.user.has_experienced_somul
            },
            "_id": speaker._id,
            "session_time": speaker.session_time,
            "introduce": speaker.introduce.replace("\n", "<br>"),
            "history": speaker.history.replace("\n", "<br>"),
            "title": speaker.title.replace("\n", "<br>"),
            "description": speaker.description.replace("\n", "<br>")
        })

    return render_template("admin/admin_matching.html",
                           speakers=list(speakers))

@admin.route("/approve")
def approve():

    secret = request.args.get('secret')

    # should write secret code
    if secret is None:
        return '', 404

    # wrong secret code
    if secret != Config.secret_auth_code:
        return '', 404

    speakers = SpeakerInfo.query.filter_by(admin_approved=0)
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

    return render_template("admin/admin_matching_approve.html",
                           speakers=list(speakers))


@admin.route("/log")
def log():
    from app.managers.credential import CredentialManager
    secret_key = CredentialManager.get_secret_key()
    results = LoggerResource().get()
    return render_template("admin/admin_log.html",
                           secret_key=secret_key,
                           results=results,
                           logs=results["items"])
