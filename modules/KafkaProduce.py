import logging

import confluent_kafka as ck
import configparser
import os
import json

# set up properties
base_dir = os.path.dirname(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(base_dir + "/resources/config.yml")

# set up logging
logging.basicConfig(level=config['Logging']['log_level'])
logger = logging.getLogger("Kafka-Producer")

bootstrap_servers = config['Kafka']['bootstrap_servers']
topic = config['Kafka']['topic']

# set up producer
producer = ck.Producer({'bootstrap.servers': bootstrap_servers})




def produce_messages(queue):
    msg_count = 0
    while True:
        try:
            msg = queue.get()
            key = msg['call_id']
            producer.produce(topic=topic, value=json.dumps(msg),
            key=str(key))
            producer.poll(0)
            queue.task_done()
            msg_count += 1
            if msg_count%100==0:
                logger.debug("Produced 100 messages successfully.")

        except Exception as E:
            logger.exception("Encountered Exception", E)
