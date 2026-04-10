import json
import logging
from fastapi import HTTPException
from confluent_kafka import Producer
from producer.schema import ProducerMessage

from constants import KAFKA_BROKER, KAFKA_TOPIC, CLIENT_ID


##### Logger

kafka_logger = 'logger-here'


##### Creating Producer

try:
    config = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': CLIENT_ID,
        'retries': 3,
        'retry.backoff.ms': 100
    }
    msg = ProducerMessage(message="Hello, Kafka!")
    producer = Producer(config)
except Exception as e:
    print("Error encountered, failed to create producer: {e}")


##### Functions

def delivery_report(err, msg):
    if err:
        print(f"Encountered error: {err}")
    else:
        print(f"Message delivered successfully: {msg.value().decode()}")
        print(f"Message metadata:\n\tTopic:{msg.topic()}\n\tPartition:{msg.partition()}\n\tOOffset:{msg.offset()}\n\tTimestamp:{msg.timestamp()}")


def msg_serializer(msg: ProducerMessage):
    return json.dumps(msg.message).encode()


def produce_kafka_msg(msg: ProducerMessage):
    value = msg_serializer(msg)
    producer.produce(
        topic = KAFKA_TOPIC,
        value = value,
        callback = delivery_report
    )
    remaining = producer.flush()
    if remaining:
        print(f"Warning: There are {remaining} remaining messages in the queue")


##### Entrypoint

if __name__=="__main__":
    produce_kafka_msg(msg)
