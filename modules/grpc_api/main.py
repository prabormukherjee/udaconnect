from __future__ import annotations

import os
import time
import grpc
import apis_pb2
import apis_pb2_grpc
from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from geoalchemy2.functions import ST_Point

from models import Person, Location

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
        
class ApiServicer(apis_pb2_grpc.ApiServiceServicer):
    def create_location(self, request, context):

        new_location = Location()
        new_location.person_id = request.person_id
        new_location.coordinate = ST_Point(request.latitude, request.longitude)
        new_location.creation_time = request.creation_time
        db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = create_engine(db_string)
        Session = sessionmaker(bind=db)
        session = Session()
        session.add(new_location)
        session.commit()
        location_request = {
            "person_id": request.person_id,
            "creation_time": request.creation_time,
            "longitude": request.longitude,
            "latitude": request.latitude,
        }
        print(location_request)
        return apis_pb2.LocationMessage(**location_request)

    def create_person(self, request, context):

        new_person = Person()
        new_person.first_name = request.first_name
        new_person.last_name = request.last_name
        new_person.company_name = request.company_name
        db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = create_engine(db_string)
        Session = sessionmaker(bind=db)
        session = Session()
        query = session.query(func.max(Person.id).label("largest_num"))
        new_person.id = (query.one().largest_num) + 1
        session.add(new_person)
        session.commit()
        person_request = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }
        
        print(person_request)
        return apis_pb2.PersonMessage(**person_request)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
apis_pb2_grpc.add_ApiServiceServicer_to_server(ApiServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)