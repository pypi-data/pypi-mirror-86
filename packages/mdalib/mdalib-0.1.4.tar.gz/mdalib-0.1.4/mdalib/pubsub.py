
# import msgpack
def test():
  print('Krit naja')
  print('DONE !!!!!')

def subscribe(option, cb):
  # TODO: validate function callback
  # TODO: handler error
  from kafka import KafkaConsumer
  import requests

  kafka_url = option["kafka_url"] or '52.77.249.163:9092'
  api_url = option["api_url"] or 'http://18.141.231.146:8000'

  print('Krit naja')
  print('kafka_url: ', kafka_url)
  print('api_url', api_url)

  resInternet = requests.get(api_url + '/internet/')
  resCall = requests.get(api_url + '/call/')
  resMessage = requests.get(api_url + '/message/')

  cb('internet_init', resInternet.json())
  cb('call_init', resCall.json())
  cb('message_init', resMessage.json())

  consumer = KafkaConsumer(
    bootstrap_servers=kafka_url,
    # value_deserializer=msgpack.loads,
  )

  consumer.subscribe(['internet_increase', 'call_increase', 'message_increase'])
  for msg in consumer:
    print('===============')
    print(msg)
    print(msg.value)
    print(msg.value.decode('utf-8'))
    cb('something_increase', msg.value.decode('utf-8'))
    print('===============')
    # assert isinstance(msg.value, dict)