import json
from confluent_kafka import Consumer

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-tracker',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)

consumer.subscribe(['order'])
print(f"Consumer running, subscribed to 'order' topic")
try:
    while True:
        msg = consumer.poll(1.0)
        if not msg:
            continue
        if msg.error():
            print(f"Error occured: {msg.error()}")
            continue
        value = msg.value().decode()
        order = json.loads(value)
        print(f"Order received: {order}")
        continue
except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected, closing consumer connection")
finally:
    consumer.close()
