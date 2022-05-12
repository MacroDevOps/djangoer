# RabbitMQ management api
import os

broker_api = 'http://{RABBITMQ_USER}:{RABBITMQ_PASSWD}@{RABBITMQ_IP}:5672/api/' \
    .format(RABBITMQ_IP=os.environ.get("RABBITMQ_IP"),
            RABBITMQ_USER=os.environ.get("RABBITMQ_USER"),
            RABBITMQ_PASSWD=os.environ.get("RABBITMQ_PASSWD")
            )

# Enable debug logging
logging = 'DEBUG'
