# Deploying AMQ Broker with secured connections (TLS)


## Red Hat Integration - AMQ Broker
Make sure the operator is installed in your namespace

## Generate certificates


Generate certificates with the following command and fill all required certs information:

IMPORTANT: For all passwords use `password`

For `"Trust this certificate? [no]` prompt type `yes`
```
$ ./gen-certs.sh
```

Create secret with the following command:
```
$ oc create secret generic ex-aao-amqp-secret \
--from-file=broker.ks=./certs/broker.ks \
--from-file=client.ts=./certs/broker.ts \
--from-literal=keyStorePassword=password \
--from-literal=truststorePassword=password
```

In this case we'll use the same certificates for MQTT as for AMQP
```
$ oc create secret generic ex-aao-mqtt-secret \
--from-file=broker.ks=./certs/broker.ks \
--from-file=client.ts=./certs/broker.ts \
--from-literal=keyStorePassword=password \
--from-literal=truststorePassword=password
```

## Deploy brokers 
Apply broker and address:
```
$ oc apply -f cr/
```

Verify the pods are up and running
```
$ oc get pods
```

