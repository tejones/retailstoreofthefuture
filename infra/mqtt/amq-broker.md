# AMQ Broker

This demo uses MQTT as the means of communication between devices and services on the Edge.

Here, we are using AMQ Broker from Red Hat Integration (https://access.redhat.com/products/red-hat-amq/)

The AMQ Broker is a messaging broker that includes support ofthe MQTT protocol. 
It is based on the Apache ActiveMQ project.

This short guide provides instructions for installing AMQ Broker on OpenShift, with the assumption that the [AMQ Broker Operator for RHEL 8](https://catalog.redhat.com/software/containers/amq7/amq-broker-rhel8-operator/5de6676fdd19c71643b76be6) has already been installed.



## Create a dedicated project
```
$ oc new-project retail-infra
```

Or use an existing project to deploy the broker.

    NOTE: AMQ Broker Operator is namespace-scoped


## Install the Broker
This guide includes [resouce definition](artemis.yaml) that can be used to create a 2-node broker with MQTT transport enabled and management console exposed:
```yaml
---
apiVersion: broker.amq.io/v1beta1
kind: ActiveMQArtemis
metadata:
  name: ex-aao
spec:
  deploymentPlan:    
    image: placeholder
    jolokiaAgentEnabled: false
    journalType: nio
    managementRBACEnabled: true
    messageMigration: false
    persistenceEnabled: false
    requireLogin: false
    size: 2
  adminPassword: admin
  adminUser: admin
  console:
    expose: true
  acceptors:
    - expose: true
      name: mqtt
      port: 1883
      protocols: mqtt
```

Please, note that the `image` field is set to `placeholder` and will be replaced by the operator with the actual (latest) image name. (See [the producer documentation](https://access.redhat.com/documentation/en-us/red_hat_amq_broker/7.10/html/deploying_amq_broker_on_openshift/deploying-broker-on-ocp-using-operator_broker-ocp#proc_br-deploying-basic-broker-operator_broker-ocp) for details.)



You can use the following command to create the broker:
```bash
$ oc apply -f artemis.yaml
```

Make sure that all the pods are up and running
```
$ oc get pods
NAME                                   READY   STATUS    RESTARTS   AGE
amq-broker-operator-5b9657b889-7qgcs   1/1     Running   0          12m
ex-aao-ss-0                            1/1     Running   0          12m
ex-aao-ss-1                            1/1     Running   0          11m
```

## Verify the installation

To verify if the MQTT Broker is working properly we can use the [Mosquitto](https://mosquitto.org/) client to connect to the broker and publish/subscribe to a topic.

Run a Mosquitto Subscriber and subscribe to focusTopic
```
oc run -it --rm mosquitto-subscriber --image=quay.io/official-images/eclipse-mosquitto -- \
mosquitto_sub -h ex-aao-mqtt-0-svc -p 1883 -t focusTopic
```

Run a Mosquitto Producer and see if messages are propagated to the subscriber
```
oc run -it --rm  --restart=Never mosquitto-producer --image=quay.io/official-images/eclipse-mosquitto -- \
mosquitto_pub -h ex-aao-mqtt-0-svc -t focusTopic -m "Test message Intel123"
```
