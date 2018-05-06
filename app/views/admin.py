from flask import render_template, Blueprint

from app.database.models import SpeakerInfo, Library
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


@admin.route("/library")
def library():
    libraries = Library.query.all()
    library_list = list()
    for library in libraries:
        library_dict = {
            "id": library._id,
            "name": library.name,
            "location": {
                "road": library.location_road,
                "detail": library.location_detail
            },
            "manager": {
                "name": library.manager_name,
                "email": library.manager_email,
                "phone": library.manager_phone
            },
            "volunteers": list(),
            "speakers": {
                "14:00": dict(),
                "15:00": dict()
            },
        }

        if library.users:
            for user in library.users:
                if user.speakerinfo:
                    library_dict["speakers"][user.speakerinfo.session_time] = {
                        "name": user.name,
                        "email": user.email,
                        "phone": user.phone,
                        "title": user.speakerinfo.title,
                        "description": user.speakerinfo.description
                        .replace("\n", "<br>"),
                        "introduce": user.speakerinfo.introduce
                        .replace("\n", "<br>"),
                        "history": user.speakerinfo.history
                        .replace("\n", "<br>"),
                        "keynote_link": user.speakerinfo.keynote_link,
                        "admin_approved": user.speakerinfo.admin_approved
                    }
                else:
                    library_dict["volunteers"].append({
                        "name": user.name,
                        "email": user.email,
                        "phone": user.phone
                    })

        library_list.append(library_dict.copy())

    return render_template("admin/admin_library_status.html",
                           libraries=library_list)


@admin.route("/log")
def log():
    results = LoggerResource().get()
    return render_template("admin/admin_log.html", logs=list(results))
