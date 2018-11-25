# kafka-streaming-calls-simulator
Application simulates real time call events and produces them into kafka.

# Running Locally
`docker-compose up -d` - Runs all the containers

# Verifying app
execute the below commands. Kafka console consumer should display incoming messages.
`   docker exec -it  calls_simulator /bin/bash
    cd /opt/kafka/bin
    ./kafka-console-consumer.sh --bootstrap-server localkafka:9092 --topic call_msgs
`


