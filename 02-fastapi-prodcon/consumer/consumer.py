import json
import uvicorn
import asyncio
from fastapi import FastAPI
from confluent_kafka import Consumer
from producer.schema import ProducerMessage

from constants import KAFKA_BROKER, KAFKA_TOPIC, KAFKA_CONSUMER_ID


stop_polling_event = asyncio.Event()
app = FastAPI()


def msg_deserialize(msg: ProducerMessage):
    if not msg:
        return
    try:
        return json.loads(msg.value().decode())
    except Exception as e:
        print(f"Unable to deserialize consumed message: {e}")
        return None


def create_consumer():

    config = {
        'bootstrap.servers': KAFKA_BROKER,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 5000,
        'group.id': KAFKA_CONSUMER_ID
    }
    consumer = Consumer(config)
    consumer.subscribe([KAFKA_TOPIC])

    return consumer


async def poll_consumer(consumer: Consumer):

    import sys
    consumer = create_consumer()
    try:
        while not stop_polling_event.is_set():
            print("Polling now...")
            records = consumer.consume(num_messages=500, timeout=5)
            if records:
                for record in records:
                    msg_str = msg_deserialize(record)
                    print(f"Received from producer.\nMessage: {msg_str}")
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("\nShutting down consumer")
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        print("Closing consumer.")
        consumer.close()


task_list = []

@app.get("/start-trigger")
async def start_polling():

    if not task_list:
        stop_polling_event.clear()
        consumer = create_consumer()
        task = asyncio.create_task(poll_consumer(consumer=consumer))
        task_list.append(task)
        return {'status':'Kafka polling has started.'}
    return {'status':'Kafka polling was already triggered.'}


@app.get("/stop-trigger")
async def stop_polling():

    stop_polling_event.set()
    if task_list:
        task_list.pop()

    return {'status':'Kafka polling has stopped.'}


if __name__=="__main__":
    # main()
    uvicorn.run("consumer.consumer:app", host="127.0.0.1", port=9003, reload_dirs=["./consumer"], reload=True)
