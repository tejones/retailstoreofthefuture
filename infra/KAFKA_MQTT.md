# Retail Infra

## Prerequisites
Operators must be available in the deployment namespace/project
1. Red Hat Integration - AMQ Streams
2. Red Hat Integration - AMQ Broker

**NOTE**: AMQ Broker Operator is namespace-scoped

## Create dedicated project for infra
```
$ oc new-project retail-infra
```

## Install Kafka

Create Kafka cluster
```
$ oc apply -f kafka/
```

Verify all pods are up and running
```
$ oc get pods
NAME                                           READY   STATUS    RESTARTS   AGE
retail-store-entity-operator-c96c856bf-5sxss   3/3     Running   0          20m
retail-store-kafka-0                           1/1     Running   0          21m
retail-store-kafka-1                           1/1     Running   0          21m
retail-store-kafka-2                           1/1     Running   0          21m
retail-store-zookeeper-0                       1/1     Running   0          21m
retail-store-zookeeper-1                       1/1     Running   0          21m
retail-store-zookeeper-2                       1/1     Running   0          21m
```

Verify Kafka cluster is working properly

1. Run Kafka consumer and subscribe to `focus-topic`
```
$ oc run -ti --rm kafka-consumer --image=quay.io/strimzi/kafka:latest-kafka-2.7.0 -- \
./bin/kafka-console-consumer.sh --bootstrap-server retail-store-kafka-bootstrap:9092 \
--topic focus-topic
```

2. In a separate window run Kafka producer
```
$ oc run -ti --rm kafka-producer --image=quay.io/strimzi/kafka:latest-kafka-2.7.0 -- \
./bin/kafka-console-producer.sh --bootstrap-server retail-store-kafka-bootstrap:9092 \
--topic focus-topic
```

When you see a command prompt type whatever you like and see if the messages are propagated to the Kafka consumer:

Producer:
```
$ oc run -ti --rm kafka-producer --image=quay.io/strimzi/kafka:latest-kafka-2.7.0 -- \
./bin/kafka-console-producer.sh --bootstrap-server retail-store-kafka-bootstrap:9092 \
--topic focus-topic 
If you don't see a command prompt, try pressing enter.
>test
>test test 123
>one two three
>
```

Consumer:
```
$ oc run -ti --rm kafka-consumer --image=quay.io/strimzi/kafka:latest-kafka-2.7.0 -- \
./bin/kafka-console-consumer.sh --bootstrap-server retail-store-kafka-bootstrap:9092 \
--topic focus-topic                                                                                                         
If you don't see a command prompt, try pressing enter.
test
test test 123
one two three
```

Default topic names:

| Event Type | Topic Name       |
|------------|------------------|
| Entry      | entry-topic      |
| Focus      | focus-topic      |
| Prediction | prediction-topic |

## Install MQTT Broker

Create MQTT Broker cluster
```
$ oc apply -f mqtt/
```


Verify all pods are up and running
```
$ oc get pods
NAME                                   READY   STATUS    RESTARTS   AGE
amq-broker-operator-5b9657b889-7qgcs   1/1     Running   0          12m
ex-aao-ss-0                            1/1     Running   0          12m
ex-aao-ss-1                            1/1     Running   0          11m
ex-aao-ss-2                            1/1     Running   0          10m
```

Verify MQTT Broker is working properly

1. Run Mosquitto Subscriber and subscribe to focusTopic
```
$ oc run -it --rm mosquitto-subscriber --image=quay.io/official-images/eclipse-mosquitto -- \
mosquitto_sub -h ex-aao-mqtt-0-svc -p 1883 -t focusTopic
```
2. Run Mosquitto Producer and see if messages are propagated to the subscriber
```
oc run -it --rm  --restart=Never mosquitto-producer --image=quay.io/official-images/eclipse-mosquitto -- \
mosquitto_pub -L mqtt://ex-aao-mqtt-2-svc:1883/focusTopic -m "Test message Intel123"
```
