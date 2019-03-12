import json
import traceback

from flask import request, render_template, session, Blueprint

from app import db
from app.database.models import Library

library = Blueprint('views.library', __name__)


def register_session(args):
    session["name"] = args["name"]
    session["location_road"] = args["roadAddress"]
    session["location_number"] = args["numberAddress"]
    session["location_detail"] = args["detailAddress"]
    session["manager_name"] = args["managerName"]
    session["manager_email"] = args["managerEmail"]
    session["manager_phone"] = args["managerPhone"]
    session["audiences"] = args["capacity"]
    session["fac_beam_screen"] = 1 if args["facilityBeamOrScreen"] else 0
    session["fac_sound"] = 1 if args["facilitySound"] else 0
    session["fac_record"] = 1 if args["facilityRecord"] else 0
    session["fac_placard"] = 1 if args["facilityPlacard"] else 0
    session["fac_self_promo"] = 1 if args["facilitySelfPromo"] else 0
    session["fac_other"] = args["facilityOther"]
    session["req_speaker"] = args["requirements"]


@library.route("/")
def index():
    return render_template("library_application.html")


@library.route("/success")
def success():
    return render_template("library_success.html")


@library.route("/failure")
def failure():
    return render_template(
        "library_failure.html",
        name=session.get("name", "정보 없음"),
        location_road=session.get("location_road", "정보 없음"),
        location_number=session.get("location_number", "정보 없음"),
        location_detail=session.get("location_detail", "정보 없음"),
        manager_name=session.get("manager_name", "정보 없음"),
        manager_email=session.get("manager_email", "정보 없음"),
        manager_phone=session.get("manager_phone", "정보 없음"),
        audiences=session.get("audiences", "정보 없음"),
        fac_beam_screen="가능" if session.get(
            "fac_beam_screen", False) else "불가",
        fac_sound="가능" if session.get("fac_sound", False) else "불가",
        fac_record="가능" if session.get("fac_record", False) else "불가",
        fac_placard="가능" if session.get("fac_placard", False) else "불가",
        fac_self_promo="가능" if session.get("fac_self_promo", False) else "불가",
        fac_other=session.get("fac_other", "정보 없음"),
        req_speaker=session.get("req_speaker", "정보 없음")
    )


@library.route("/applylist")
def applylist():
    # TODO(@harrydrippin): Basic Authentication 적용
    try:
        libraries = Library.query.all()

        return render_template("library_list.html",
                               libraries=libraries,
                               length=len(list(libraries)))
    except:  # noqa: E722
        print(traceback.format_exc())


@library.route("/apply", methods=['GET', "POST"])
def apply():
    try:
        args = json.loads(request.data.decode('utf-8'))
    except:  # noqa: E722
        print("Invalid Request Payload")
        return json.dumps({
            "result": -1,
            "cause": "Invalid request payload"
        })

    register_session(args)

    db.session.add_all([
        Library(
            name=args["name"],
            location_road=args["roadAddress"],
            location_number=args["numberAddress"],
            location_detail=args["detailAddress"],
            manager_name=args["managerName"],
            manager_email=args["managerEmail"],
            manager_phone=args["managerPhone"],
            audiences=args["capacity"],
            fac_beam_screen=1 if args["facilityBeamOrScreen"] else 0,
            fac_sound=1 if args["facilitySound"] else 0,
            fac_record=1 if args["facilityRecord"] else 0,
            fac_placard=1 if args["facilityPlacard"] else 0,
            fac_self_promo=1 if args["facilitySelfPromo"] else 0,
            fac_other=args["facilityOther"],
            req_speaker=args["requirements"]
        )
    ])

    try:
        db.session.commit()

        return json.dumps({
            "result": 0
        })
    except:  # noqa: E722
        db.session.rollback()
        print("Unexpected DB server error")
        return json.dumps({
            "result": 1,
            "cause": "Unexpected DB server error"
        })
