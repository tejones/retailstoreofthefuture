#! /bin/bash

WORKDIR="./certs"
mkdir -p $WORKDIR

echo "=== Generating Broker keystore ==="
keytool -genkey -alias broker -keyalg RSA -keystore $WORKDIR/broker.ks
echo "=== Exporting Broker certificate ==="
keytool -export -alias broker -keystore $WORKDIR/broker.ks -file $WORKDIR/broker_cert
echo "=== Generating Client keystore ==="
keytool -genkey -alias client -keyalg RSA -keystore $WORKDIR/client.ks
echo "=== Importing Broker certificate to Client Truststore ==="
keytool -import -alias broker -keystore $WORKDIR/client.ts -file $WORKDIR/broker_cert
echo "=== Exporting Client certificate ==="
keytool -export -alias client -keystore $WORKDIR/client.ks -file $WORKDIR/client_cert
echo "=== Importing Client certificate to Broker Truststore ==="
keytool -import -alias client -keystore $WORKDIR/broker.ts -file $WORKDIR/client_cert

openssl x509 -inform DER -in $WORKDIR/client_cert -out $WORKDIR/client.pem -outform PEM
openssl x509 -inform DER -in $WORKDIR/broker_cert -out $WORKDIR/broker.pem -outform PEM