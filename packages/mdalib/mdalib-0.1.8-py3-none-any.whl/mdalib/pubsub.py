def default_cb():
  return

def subscribe(option = {}, cb = default_cb):
  # TODO: validate function callback
  # TODO: handler error
  from kafka import KafkaConsumer
  import requests

  kafka_url = option["kafka_url"]
  api_url = option["api_url"]

  print('Krit naja')
  print('kafka_url: ', kafka_url)
  print('api_url', api_url)

  resInternet = requests.get(api_url + '/internet/')
  resCall = requests.get(api_url + '/call/')
  resMessage = requests.get(api_url + '/message/')

  print("==== from API ====")
  cb('internet', resInternet.json())
  cb('call', resCall.json())
  cb('message', resMessage.json())

  consumer = KafkaConsumer(
    bootstrap_servers=kafka_url,
    # value_deserializer=msgpack.loads,
  )

  # consumer.subscribe(['internet_increase'])
  consumer.subscribe(['internet_increase', 'call_increase', 'message_increase'])
#   consumer.subscribe(['test'])
  for msg in consumer:
    print("==== from stream ====")
    cb(msg.topic, [msg.value.decode('utf-8')])

# def test(topic, val):
#   # print(topic, val)
#   print("============")
#   print(topic)


# option = {
#   "kafka_url": "3.1.209.161:9092",
#   "api_url": "http://fe2c56bb5e52.ngrok.io"
# }

# subscribe(option, cb=test)

# from kafka import KafkaConsumer
# consumer = KafkaConsumer(
#   bootstrap_servers="3.1.209.161:9092",
#   # value_deserializer=msgpack.loads,
# )
# consumer.subscribe(['test'])
# for msg in consumer:
#   print('===============')
#   print(msg)
#   print(msg.value)
#   print(msg.value.decode('utf-8'))
#   # cb('something_increase', [msg.value.decode('utf-8')])
#   print('===============')

# from confluent_kafka import Consumer

# from confluent_kafka import Consumer

# running = True


# def basic_consume_loop(consumer, topics):
#     try:
#         consumer.subscribe(topics)

#         while running:
#             msg = consumer.poll(timeout=1.0)
#             if msg is None:
#                 continue

#             if msg.error():
#                 if msg.error().code() == KafkaError._PARTITION_EOF:
#                     # End of partition event
#                     sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
#                                      (msg.topic(), msg.partition(), msg.offset()))
#                 elif msg.error():
#                     raise KafkaException(msg.error())
#             else:
#                 msg_process(msg)
#     finally:
#         # Close down consumer to commit final offsets.
#         consumer.close()


# def shutdown():
#     running = False

# conf = {
#     'bootstrap.servers': "3.1.209.161:9092",
#     'group.id': "foo",
#     'auto.offset.reset': 'smallest'
# }

# consumer = Consumer(conf)

# basic_consume_loop(consumer, ['test'])
