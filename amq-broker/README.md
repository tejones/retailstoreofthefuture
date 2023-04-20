# MQTT on OpenShift with AMQ Broker

This demo uses MQTT as the means of communication between devices and services on the Edge. 

MQTT is a lightweight messaging protocol that is designed for constrained devices and low-bandwidth, high-latency or unreliable networks. MQTT is a publish/subscribe protocol, which means that clients can both publish messages to a topic and subscribe to topics to receive published messages. MQTT is a very simple protocol, which makes it easy to implement. It is also very lightweight, which makes it suitable for use on low-power devices with limited network bandwidth.

This project demonstrates how to use MQTT on OpenShift with AMQ Broker.

Topics covered:
- Configuring AMQ Broker for secured MQTT communication
- Using MQTT protocol version 5 (MQTTv5), including shared subscriptions, on OpenShift with AMQ Broker.


## MQTT v5
MQTT version 5, an OASIS standard that was released in March 2019, offers a variety of enhancements over its previous version, MQTT 3.1.1. These improvements can bring significant benefits to users. Detailed information about these enhancements can be found in the official specification at https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901293.

Enhancements for scalability and large scale systems, performance improvements, better error handling, more "sophisticated" communication patterns (request-response, shared subscription) are some of the benefits of MQTT v5. Here, we'll demonstrate how to achieve client load balancing using shared subscriptions.

The latest verision of AMQ Broker (7.10 ATTOW) contains ActiveMQ Artemis 2.21.0 wich bring support for MQTT v5.
See: _[Client load balancing](client-load-balancing)_ for required configuration and example python code.

