import logging
from typing import Dict, List

from app import db
from app.persons.models import Person
from app.persons.schemas import PersonSchema
from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()

    @staticmethod
    def create_person_kafka_queue(person: Dict) -> Person:
        validation_results: Dict = PersonSchema().validate(person)
        if validation_results:
            logger.warning(f"Data received in unknown format: {validation_results}")
            raise Exception(f"Unknown data: {validation_results}")

        TOPIC_NAME = 'person_api'
        KAFKA_SERVER = 'kafka:9092'
        person_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        person_producer.send(TOPIC_NAME, bytes(str(person), 'utf-8'))
        person_producer.flush()
