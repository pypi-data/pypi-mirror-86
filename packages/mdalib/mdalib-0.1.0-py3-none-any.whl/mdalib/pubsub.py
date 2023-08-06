
# import msgpack
def test():
  print('DONE !!!!!')

def subscribe(cb):
  # TODO: validate function callback
  # TODO: handler error
  from kafka import KafkaConsumer
  import requests

  consumer = KafkaConsumer(
    bootstrap_servers="52.77.249.163:9092",
    # value_deserializer=msgpack.loads,
  )

  consumer.subscribe(['information'])
  resInternet = requests.get('http://18.141.231.146:8000/internet/')
  resCall = requests.get('http://18.141.231.146:8000/call/')
  resMessage = requests.get('http://18.141.231.146:8000/message/')

  cb(resInternet.json())
  cb(resCall.json())
  cb(resMessage.json())

  for msg in consumer:
    print("===============")
    print(msg.value)
    print(msg.value.decode('utf-8'))
    cb(msg.value.decode('utf-8'))
    print("===============")
    # assert isinstance(msg.value, dict)