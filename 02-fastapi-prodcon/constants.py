from socket import gethostname

CLIENT_ID = gethostname()
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'kafka.topic.fapi'
KAFKA_ADMIN_CLIENT = 'kafka.adminclient.fapi'
