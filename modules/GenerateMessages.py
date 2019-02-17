import configparser
import os
import logging
import random
import math
from datetime import datetime, timedelta
from modules import generate_random_msg, generate_customer_id
import time

# Read from default config
base_dir = os.path.dirname(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(base_dir + "/resources/config.yml")

# set up logging
logging.basicConfig(level=config['Logging']['log_level'])
logger = logging.getLogger("Message-Generator")

# set up generation inputs
period_duration = int(config['Application']['PeriodDurationInSeconds'])
period_events_count = int(config['Application']['PeriodEvents'])
gen_start_time = (datetime.now() + timedelta(seconds=period_duration * -1))
gen_end_time = datetime.strptime(config['Application']['EndTime'], '%d-%m-%Y %H:%M:%S')


logger.info("Start time: " + str(gen_start_time))
logger.info("End Time: " + str(gen_end_time))
logger.info("Period Duration " + str(period_duration))
logger.info("Period Events " + str(period_events_count))


def generate_messages(queue):
    current_time = gen_start_time
    next_period_start_time = current_time + timedelta(seconds=period_duration)
    msg_count = 0
    while current_time < gen_end_time:
        if current_time >= next_period_start_time or current_time == gen_start_time:
            next_period_start_time = current_time + timedelta(seconds=period_duration)
            logger.debug("Generating messages between " + str(current_time) + " to " + str(next_period_start_time))
            repeat_customer_count = 2
            repeat_customer_msgs = 0

        if repeat_customer_count > 0 and repeat_customer_msgs == 0:
            repeat_customers = generate_customer_id()
            repeat_customer_msgs = random.randint(5, 15)
            repeat_customer_mod = math.floor(period_events_count / repeat_customer_count / repeat_customer_msgs)
            repeat_customer_count -= 1
            logger.debug("The customer + " + str(repeat_customers) + " calls repeatedly for " + str(repeat_customer_msgs) + " in the current period.")


        if msg_count % repeat_customer_mod == 0 and repeat_customer_msgs > 0:
            queue.put(generate_random_msg(current_time, repeat_customers))
            repeat_customer_msgs -= 1
        else:
            queue.put(generate_random_msg(current_time))

        current_time = current_time + timedelta(seconds=period_duration/period_events_count)

        if current_time>datetime.now():
            sleep_duration = (current_time-datetime.now()).total_seconds()
            if sleep_duration < 0:
                sleep_duration=0
            time.sleep(sleep_duration)