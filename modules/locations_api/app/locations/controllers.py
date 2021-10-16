from datetime import datetime

from app.locations.models import Location
from app.locations.schemas import (
    LocationSchema,
)
from app.locations.services import LocationService
from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("locations_api", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        LocationService.create_message_kafka_queue(request.get_json())
        return Response(status=202)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
