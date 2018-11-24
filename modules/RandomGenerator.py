import random
import math
import numpy as np
import string
from datetime import  datetime, timedelta

counter = {"call_id": 0, "call_group_id": 0}

call_duration = np.arange(60, 1801, 60, int)
call_duration_probability = np.flip(call_duration)/call_duration.sum()

queue_duration_percentage = np.arange(0.1, 1, 0.1, float)
queue_duration_percentage_probability = np.flip(queue_duration_percentage)/queue_duration_percentage.sum()

# Sometimes the probabilities in python don't add to 1.0. Hence need to normalize probabilities.
success = 0
while success == 0:
    try:
        np.random.choice(call_duration, p=call_duration_probability)
        success = 1
    except ValueError:
        call_duration_probability = np.flip(call_duration) / call_duration.sum()
        pass

# Sometimes the probabilities in python don't add to 1.0. Hence need to normalize probabilities.
success = 0
while success == 0:
    try:
        np.random.choice(queue_duration_percentage, p=queue_duration_percentage_probability)
        success = 1
    except ValueError:
        queue_duration_percentage_probability = np.flip(queue_duration_percentage)/queue_duration_percentage.sum()
        pass

departments = ["Orders", "Billings", "Service", "Delivery_Returns", "Others"]
products = ["TV", "Phone", "Computer"]
call_reason = {
    'Orders' : ["Order not generated", "Order Incorrect", "Telephone Order", "Order Cancellation", "Pre order", "Order Modification"],
    'Billings' : ["Bill not generated", "Bill Incorrect", "Advance Bill payment"],
    "Service" : ["Service Disruption" , "Service Cancellation", "New Service", "Service Enquiry"],
    "Delivery_Returns" : ["Return Order", "Delivery Information", "Schedule Delivery", "Product Not Delivered", "Partial Delivery", "Damaged Delivery", "Delayed Delivery", "Refund"],
    "Others" : ["Online site not working"]
}


def generate_call_id():
    counter['call_id'] += 1
    return counter['call_id']


def generate_call_group_id():
    counter['call_group_id'] += 1
    return counter['call_group_id']


def generate_call_duration():
    return np.random.choice(call_duration, p=call_duration_probability).item()


def generate_queue_duration(p_call_duration):
    v_queue_duration_percentage = np.random.choice(queue_duration_percentage, p=queue_duration_percentage_probability).item()
    return math.floor(p_call_duration * v_queue_duration_percentage)


def generate_department():
    return random.choice(departments)


def generate_product():
    return random.choice(products)


def generate_call_reason(department):
    return random.choice(call_reason.get(department))


def generate_customer_id():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for n in range(15)),


def generate_message_timestamp(current_time):
    message_timestamps = dict()
    v_call_duration = generate_call_duration()
    v_call_start_time = current_time + timedelta(seconds=v_call_duration * -1)
    v_queue_start_time = v_call_start_time + timedelta(seconds=5)
    v_queue_duration = generate_queue_duration(v_call_duration)
    v_queue_end_time = v_queue_start_time + timedelta(seconds=v_queue_duration - 5)
    v_handling_duration = v_call_duration - v_queue_duration
    if v_handling_duration > 0:
        v_handling_start_time = v_queue_end_time + timedelta(seconds=1)
        v_handling_end_time = v_handling_start_time + timedelta(seconds=v_handling_duration -1)
    else:
        v_handling_start_time = ""
        v_handling_end_time = ""
    v_call_end_time = current_time
    message_timestamps["call_start_time"] = v_call_start_time
    message_timestamps["call_queue_start_time"] = v_queue_start_time
    message_timestamps["call_queue_end_time"] = v_queue_end_time
    message_timestamps["call_handling_start_time"] = v_handling_start_time
    message_timestamps["call_handling_end_time"] = v_handling_end_time
    message_timestamps["call_end_time"] = v_call_end_time
    return message_timestamps


def generate_random_msg(current_time, p_customer_id=None):
    message = dict()
    message['call_id'] = generate_call_id()
    message['call_group_id'] = generate_call_group_id()
    message_timestamps = generate_message_timestamp(current_time)
    message['call_start_time'] = message_timestamps.get('call_start_time')
    message['call_queue_start_time'] = message_timestamps.get('call_queue_start_time')
    message['call_queue_end_time'] = message_timestamps.get('call_queue_end_time')
    message['call_handling_start_time'] = message_timestamps.get('call_handling_start_time')
    message['call_handling_end_time'] = message_timestamps.get('call_handling_end_time')
    message['call_end_time'] = message_timestamps.get('call_end_time')
    v_department = generate_department()
    message['department'] = v_department
    if p_customer_id is None:
        message['customer_id'] = generate_customer_id()
    else:
        message['customer_id'] = p_customer_id
    message['product'] = generate_product()
    message['call_reason'] = generate_call_reason(v_department)
    return message