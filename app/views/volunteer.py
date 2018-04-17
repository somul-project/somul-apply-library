from flask import render_template, Blueprint, redirect

from app.managers.signin import SigninManager
from app.database.models import User, Library

volunteer = Blueprint('views.volunteer', __name__)


@volunteer.route("/")
def application():
    if SigninManager.get_is_signed_in():
        return redirect("/volunteer/information")

    return render_template("volunteer/application.html")


@volunteer.route("/login")
def status():
    if SigninManager.get_is_signed_in():
        return redirect("/volunteer/information")
    return render_template("volunteer/login.html")


@volunteer.route("/success")
def success():
    return render_template("volunteer/application_success.html")


@volunteer.route("/privacy_policy")
def privacy_policy():
    return render_template("volunteer/privacy_policy.html")


@volunteer.route("/information")
def information():
    if not SigninManager.get_is_signed_in():
        return redirect("/volunteer/login")

    user = User.query.filter_by(_id=SigninManager.get_user_id()).first()
    speakerinfo = user.speakerinfo if user.speakerinfo else None

    return render_template("volunteer/information.html",
                           user=user,
                           speakerinfo=speakerinfo
                           )


@volunteer.route("/speaker_info")
def information_modify():
    if not SigninManager.get_is_signed_in():
        return redirect("/volunteer/login")

    user = User.query.filter_by(_id=SigninManager.get_user_id()).first()
    return render_template("volunteer/additional_info.html",
                           speaker=user.speakerinfo)


@volunteer.route("/modify")
def modify_user():
    if not SigninManager.get_is_signed_in():
        return redirect("/volunteer/login")

    user = User.query.filter_by(_id=SigninManager.get_user_id()).first()
    return render_template("volunteer/modify_user.html",
                           user=user)


MATCH_AVAILABLE = 0
MATCH_RESERVED = 1
MATCH_NOT_AVAILABLE = 2


@volunteer.route("/match")
def library_list():
    if not SigninManager.get_is_signed_in():
        return redirect("/volunteer/login")

    user = User.query.filter_by(_id=SigninManager.get_user_id()).first()
    if user.library_id is not None:
        return redirect("/volunteer/information")

    libraries = Library.query.all()

    lib_dict = dict()

    for library in libraries:
        session_dict = {
            "name": library.name,
            "location": library.location_road,
            "14:00": 0,
            "15:00": 0,
            "volunteer": 0
        }

        for user in library.users:
            if user.speakerinfo:
                time = user.speakerinfo.session_time
                admin_approved = user.speakerinfo.admin_approved
                if admin_approved == 0:
                    availability = 2
                elif admin_approved is None or admin_approved == 1:
                    availability = 1
                else:
                    availability = 0

                session_dict[time] = availability
            else:
                session_dict["volunteer"] += 1

        lib_dict[library._id] = session_dict.copy()

    print(lib_dict)

    return render_template("volunteer/match.html",
                           libraries=libraries, lib_dict=lib_dict)
