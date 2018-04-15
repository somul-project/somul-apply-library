from flask import render_template, Blueprint
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from app.database.models import VerifyEmail, now_at_seoul, \
    elapsed_datetime_at_seoul
from app.database import db
from app.utils.errors import abort_with_integrityerror

verify = Blueprint('views.verify', __name__)

verify_reqparser = reqparse.RequestParser()
verify_reqparser.add_argument("key", type=str, trim=True,
                              location=['args'], required=True,
                              nullable=False,
                              help="No key information provided")


@verify.route("")
def verify_email():
    args = verify_reqparser.parse_args()
    email = VerifyEmail.query.filter_by(key=args["key"]).first()
    if email is None:
        return "적절한 Key가 아닙니다. 운영자에게 문의해주시기 바랍니다."

    if email.expired:
        return "이미 만료된 링크입니다."

    if elapsed_datetime_at_seoul(email.sended_at).days > 0:
        email.expired = True

        try:
            db.session.merge(email)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return "24시간이 초과하여 회원 가입 이력이 삭제되었습니다. 다시 가입해주세요."

    email.verified_at = now_at_seoul()
    email.is_verified = True
    email.expired = True
    try:
        db.session.merge(email)
        db.session.commit()
    except IntegrityError as e:
        print(str(e))
        db.session.rollback()
        abort_with_integrityerror(e)
    except Exception as e:
        print(str(e))
        db.session.rollback()
        raise e

    return "인증이 완료되었습니다."
