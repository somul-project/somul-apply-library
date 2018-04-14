from flask import render_template, Blueprint

from app import db
from app.database.models import Library

admin = Blueprint('views.admin', __name__)

@admin.route("/")
def index():
    return render_template("admin_matching.html")
