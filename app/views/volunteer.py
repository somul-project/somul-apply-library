from flask import render_template, Blueprint


volunteer = Blueprint('views.volunteer', __name__)


@volunteer.route("/")
def application():
    return render_template("volunteer/application.html")
