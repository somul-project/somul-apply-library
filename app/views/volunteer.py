from flask import render_template, Blueprint


volunteer = Blueprint('views.volunteer', __name__)


@volunteer.route("/")
def application():
    return render_template("volunteer/application.html")


@volunteer.route("/status")
def status():
    return render_template("volunteer/application_status.html")


@volunteer.route("/success")
def success():
    return render_template("volunteer/application_success.html")


@volunteer.route("/privacy_policy")
def privacy_policy():
    return render_template("volunteer/privacy_policy.html")


@volunteer.route("/information")
def information():
    return render_template("volunteer/information.html")


@volunteer.route("/library_list")
def library_list():
    return render_template("volunteer/library_list.html")
