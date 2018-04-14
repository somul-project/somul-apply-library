from flask import render_template, Blueprint

admin = Blueprint('views.admin', __name__)


@admin.route("/")
def index():
    return render_template("admin_matching.html")
