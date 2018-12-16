from kafka import KafkaConsumer
import kafka
import confluent_kafka as ck
import json
import csv

consumer = KafkaConsumer()
consumer = KafkaConsumer('call_msgs',
                         bootstrap_servers=['localhost:9092'])


for msg in consumer:
    print(json.loads(msg.value))
