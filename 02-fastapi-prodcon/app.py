from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from confluent_kafka.admin import AdminClient
from producer.schema import ProducerMessage
from producer.producer import produce_kafka_msg

from constants import KAFKA_BROKER, KAFKA_TOPIC, KAFKA_ADMIN_CLIENT


@asynccontextmanager
async def lifespan(app: FastAPI):

    admin_client = AdminClient({
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': KAFKA_ADMIN_CLIENT
    })

    topics_available = admin_client.list_topics()

    if KAFKA_TOPIC not in topics_available.topics:
        admin_client.create_topics(
            new_topics = [
                admin_client.NewTopic(
                    topic = KAFKA_TOPIC,
                    num_partitions = 1,
                    replication_factor = 1
                )
            ],
            validate_only = False
        )
    yield

def add_routes():

    @app.post("/produce/message", tags=["Produce Message"])
    async def produce_message(messageRequest: ProducerMessage, background_tasks: BackgroundTasks):
        background_tasks.add_task(produce_kafka_msg, messageRequest)
        return {'message':'Message received.'}

app = FastAPI(lifespan=lifespan)
add_routes()
