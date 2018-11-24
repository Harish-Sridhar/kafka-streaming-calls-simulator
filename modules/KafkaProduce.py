import confluent_kafka as ck
import configparser
import os

# set up properties
base_dir = os.path.dirname(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(base_dir + "/resources/config.yml")

bootstrap_servers = config['Kafka']['bootstrap_servers']
topic = config['Kafka']['topic']

# set up producer
producer = ck.Producer({'bootstrap.servers': bootstrap_servers})

def produce_messages(queue):
    while True:
        msg=queue.get()
        key=msg['call_id']
        producer.produce(topic=topic, value=msg,
                         key=key)
        producer.poll(0)
        queue.task_done()