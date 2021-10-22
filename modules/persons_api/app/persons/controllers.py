from datetime import datetime

from app.persons.models import Person
from app.persons.schemas import (
    PersonSchema,
)
from app.persons.services import PersonService
from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("persons_api", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        PersonService.create_person_kafka_queue(payload)
        return Response(status=202)

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
