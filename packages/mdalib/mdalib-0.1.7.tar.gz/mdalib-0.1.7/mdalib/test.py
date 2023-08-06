# from kafka import KafkaProducer
# import json
from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "3.1.209.161:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)
producer.produce("test", key="key", value="value")

# producer = KafkaProducer(
#   # bootstrap_servers="52.77.249.163:9092",
#   bootstrap_servers="3.1.209.161:9092",
#   value_serializer=lambda v: json.dumps(v).encode("utf-8")
# )

# aa = {"a", "i="}
# for i in range(10):
#   print("send ===========")
#   producer.send('test', "sssss")
