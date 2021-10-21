import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.locations.models import Location
from app.locations.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locations-api")

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location

    @staticmethod
    def create_location_kafka_queue(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Data received in unknown format: {validation_results}")
            raise Exception(f"Unknown data: {validation_results}")
        TOPIC_NAME = 'location_api'
        KAFKA_SERVER = 'kafka:9092'
        location_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        location_producer.send(TOPIC_NAME, bytes(str(location), 'utf-8'))
        location_producer.flush()
