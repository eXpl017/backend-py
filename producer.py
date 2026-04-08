import json
import uuid
from confluent_kafka import Producer


producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_config)


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivery succeeded - {msg.value().decode()}")
        print(f"All message fields - {dir(msg)}")

order = {
    "order_id": str(uuid.uuid4()),
    "user": "random name",
    "item": "random item",
    "quantity": 4
}

value = json.dumps(order).encode('utf-8')
producer.produce(
    topic='order',
    value=value,
    callback=delivery_report
)
producer.flush()
