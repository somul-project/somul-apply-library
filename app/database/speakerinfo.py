from sqlalchemy.exc import IntegrityError

from app.database import db, get_or_none
from app.database.models import SpeakerInfo
from app.utils.errors import abort_with_integrityerror


class SpeakerInfoRepo:
    @classmethod
    def insert(cls, args):
        speakerinfo = SpeakerInfo(**args)

        try:
            db.session.add(speakerinfo)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        return speakerinfo

    @classmethod
    def update(cls, speakerinfo, args):
        for key, value in args.items():
            if value is None:
                continue

            setattr(speakerinfo, key, value)

        try:
            db.session.merge(speakerinfo)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort_with_integrityerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

        print(speakerinfo)

        return speakerinfo

    @classmethod
    def get_with_user_id(cls, user_id):
        return get_or_none(SpeakerInfo, user_id)

    @classmethod
    def delete(cls, speakerinfo):
        try:
            db.session.delete(speakerinfo)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e
