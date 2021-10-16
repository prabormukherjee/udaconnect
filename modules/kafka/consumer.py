import grpc
import apis_pb2
import apis_pb2_grpc
from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-consumer")

TOPIC_NAME = 'person_api'
KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER], value_deserializer=lambda m: json.dumps(m.decode('utf-8')))


channel = grpc.insecure_channel("udaconnect-grpc:5005")
stub = apis_pb2_grpc.ApiServiceStub(channel)

for message in consumer:
    json_message=eval(json.loads((message.value)))
    
    if "person_id" in json_message:
        location = apis_pb2.LocationMessage(
            person_id=json_message["person_id"],
            creation_time=json_message["creation_time"],
            longitude=json_message["longitude"],
            latitude=json_message["latitude"]
        )
        stub.create_location(location)
    elif "first_name" in json_message:
        person = apis_pb2.PersonMessage(
            first_name=json_message["first_name"],
            last_name=json_message["last_name"],
            company_name=json_message["company_name"]
        )
        stub.create_person(person)
    else:
        logger.info("What are you looking for??")
    