from flask import Blueprint
from flask_restful import (Resource, fields, marshal_with,
                           Api)

from app.database.models import Library

map_fields = {
    '_id': fields.Integer,
    'name': fields.String,
    'location_road': fields.String,
    'province': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
}


class MapListResource(Resource):
    def __init__(self):
        super().__init__()

    @marshal_with(map_fields)
    def get(self):
        libraries = Library.query.all()

        for library in libraries:
            if library.location_road:
                library.province = library.location_road[0:2]

        return libraries


maps_api = Blueprint('resources.maps', __name__)
api = Api(maps_api)
api.add_resource(
    MapListResource,
    '',
    endpoint='maps'
)
