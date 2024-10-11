import socket
import json
import threading
from kafka import KafkaProducer, KafkaConsumer

class StreamService:
    def __init__(self, kafka_bootstrap_servers, kafka_topic, type="producer"):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic
        if type == "producer":
            self.stream = KafkaProducer(
                bootstrap_servers=kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                security_protocol="SASL_SSL",
                sasl_mechanism="SCRAM-SHA-256",
                sasl_plain_username="feedbeat",
                sasl_plain_password="FYfqZhhPh51BICVUR0EXPmAcgPElWt"
            )
        elif type == "consumer":
            self.stream = KafkaConsumer(
                bootstrap_servers=kafka_bootstrap_servers,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                security_protocol="SASL_SSL",
                sasl_mechanism="SCRAM-SHA-256",
                sasl_plain_username="feedbeat",
                sasl_plain_password="FYfqZhhPh51BICVUR0EXPmAcgPElWt",
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                consumer_timeout_ms=10000
            )
            self.stream.subscribe(kafka_topic)
        else:
            raise ValueError("Invalid type")

    def send_message(self, message, hostname=None):
        if hostname is None:
            hostname = socket.gethostname()

        self.stream.send(self.kafka_topic, key=hostname.encode('utf-8'), value=message)

    def consume_message(self):
        array = []
        for message in self.stream:
            array.append(message.value)
        print(array)
        return array
        
    def flush(self):
        self.stream.flush()

    def close(self):
        self.stream.close()

    # def __del__(self):
    #     self.flush()
    #     self.close()


def get_stream_service(kafka_bootstrap_servers, kafka_topic, type):
    return StreamService(kafka_bootstrap_servers, kafka_topic, type)

