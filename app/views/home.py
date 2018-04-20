from flask import render_template, Blueprint

home = Blueprint('views.home', __name__)


@home.route("/")
def index():
    return render_template("home.html")
