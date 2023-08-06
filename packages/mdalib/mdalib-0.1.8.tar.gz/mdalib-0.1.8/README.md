# MDA streaming library

`สวัสดีนี่กิตเอง`

## Install

```bash
pip install mdalib
```

`require: kafka-python, msgpack, requests`

## Method

```python
import mdalib


def test(topic, val):
  print(topic)
  print(val)
  # TODO: implement this

option = { # for development
  "kafka_url": SOME_KAFKA_URL, 
  "api_url": SOME_API_URL
}

mdalib.subscribe(option, cb=test)
```

ชื่อ topic | ความหมาย
-------- | --------
`message` | ข้อมูล message จาก API
`message_increase` | ข้อมูล message จาก Streaming
`internet` | ข้อมูล internet จาก API
`internet_increase` | ข้อมูล internet จาก Streaming
`call` | ข้อมูล call จาก API
`call_increase` | ข้อมูล call จาก Streaming
