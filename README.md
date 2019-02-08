# kafka-streaming-calls-simulator
Application simulates real time call events and produces them into kafka.

# How it works
The application divides the start time and end time into smaller periods.
Per each period, it generates a fixed number of events.
If the period that it is generating is in the past, it generates the messages without any waiting time.
If the period that it is generating is in the future, it generates at real time.
Each period, it selects 2 customers randomly and generates repeat calls.


# Application Configuration
|Config parameter | Description |
|-----------------|-------------|
|StartTime        | The start time of the message generation.|
|EndTime          | End time of the message generation.      |
|PeriodDurationInSeconds| How long does a period last        |
|PeriodEvents | How many events to produce in a period       |


# What uses cases can we solve with this
1. Calculate total time it takes to handle a customer call.
2. Calculate top 5 call reasons.
3. Find out the repeated caller.
4. Find out anomalous calls by certain rules:
    1. if a call duration is high.
    2. if a call is from a repeated customer.
    3. if a call ends in a queue.
5. Sum of the following:
    1. total calls handled.
    2. total calls disconnected.
    3. average handling time.
    4. average queue time.
    5. average call duration.
    6. total number of repeated customers.


# Running Locally
`docker-compose up -d` - Runs all the containers

# Verifying app
execute the below commands. Kafka console consumer should display incoming messages.
```
   docker exec -it  localkafka /bin/bash
   cd /opt/kafka/bin
   ./kafka-console-consumer.sh --bootstrap-server localkafka:9092 --topic call_msgs
```


