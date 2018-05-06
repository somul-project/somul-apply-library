from flask import Blueprint
from flask_restful import (Resource, Api)

from app.database.models import Library


class MapListResource(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        libraries = Library.query.all()

        library_list = list()
        for library in libraries:
            library_dict = {
                "id": library._id,
                "name": library.name,
                "location": {
                    "road": library.location_road,
                    "detail": library.location_detail,
                    "latitude": str(library.latitude),
                    "longitude": str(library.longitude)
                },
                "volunteers": list(),
                "speakers": {
                    "14:00": dict(),
                    "15:00": dict()
                }
            }

            if library.users:
                for user in library.users:
                    if user.speakerinfo:
                        sess_time = user.speakerinfo.session_time
                        library_dict["speakers"][sess_time] = {
                            "name": user.name,
                            "email": user.email,
                            "title": user.speakerinfo.title,
                            "description": user.speakerinfo.description
                            .replace("\n", "<br>"),
                            "introduce": user.speakerinfo.introduce
                            .replace("\n", "<br>"),
                            "history": user.speakerinfo.history
                            .replace("\n", "<br>")
                            # "keynote_link": user.speakerinfo.keynote_link
                        }
                    else:
                        library_dict["volunteers"].append({
                            "name": user.name,
                            "email": user.email
                        })

            library_list.append(library_dict.copy())

        return library_list


maps_api = Blueprint('resources.maps', __name__)
api = Api(maps_api)
api.add_resource(
    MapListResource,
    '',
    endpoint='maps'
)
