# Development

This document describes development techniques that can improve and fasten this process.
Here you can find information corelated with more than one component.
There might be some additional data

## Table of contents

* [Deploy and set up external components](#deploy-and-set-up-external-components)
  * [Testing with Kafka in docker](#testing-with-kafka-in-docker)
  * [Testing with MQTT broker in docker](#testing-with-mqtt-broker-in-docker)
  * [Testing with Postgres in docker](#testing-with-postgres-in-docker)

## Deploy and set up external components

The solution uses external services and componets:

* Kafka/OpenShift Streams
* MQTT/AMQ Broker
* Postgres database

For development purposes components can be deployed localy with Docker containers.

Prerequsitions:

* Docker installed
* docker-compose installed

### Testing with Kafka in docker

You may need this setup to test:

* Quarkus/MQTT->Kafka bridge

#### Setup

One of the quickest way to set up Kafka cluster for development purposes is to use Docker containers.

The procedure to **set up the cluster** boils down to:

```shell
curl --silent --output docker-compose.yml \
  https://raw.githubusercontent.com/confluentinc/cp-all-in-one/6.1.0-post/cp-all-in-one/docker-compose.yml

docker-compose up -d
```

See https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html for the details.

To **create a topic**:

```shell
docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic ENTRY_EVENT
```

where

* `broker` is the name of the container hosting Kafka broker instance
* `localhost:9092` is the broker's URL
* `ENTRY_EVENT` is the topic name

To **produce some testing messages**, one can issue the following command:

```shell
docker-compose exec broker \
  bash -c "seq 10 | kafka-console-producer --request-required-acks 1 --broker-list localhost:9092 --topic ENTRY_EVENT && echo 'Produced 10 messages.'"
```
or   
```shell
docker-compose exec broker \
  bash -c "echo '{\"event_type\":\"customer focus\",\"event_timestamp\":\"2001-12-17T09:30:47.0\",\"payload\":{\"customer_id\":3,\"category\":\"Boys\"}}' | kafka-console-producer --request-required-acks 1 --broker-list localhost:9092 --topic FOCUS_EVENTS && echo 'Message produced.'"
```

where

* `broker` is the name of the container hosting Kafka broker instance
* `ENTRY_EVENT` is the topic name
* `localhost:9092` is the broker's URL

### Testing with MQTT broker in docker

You may need this setup to test:

* Recommendation Service
* Visualization Application
* Mobile Application
* Scenario Player

#### Setup

To **run the container** with mosquitto broker:

```shell
docker run -d --rm --name mosquitto -p 1883:1883 eclipse-mosquitto
```
or
```shell
docker run -it -p 1883:1883 --name mosquitto eclipse-mosquitto mosquitto -c /mosquitto-no-auth.conf
```

To **publish to a topic**:

```shell
docker exec mosquitto mosquitto_pub -h 127.0.0.1 -t test -m "test message"
```

To **subscribe to a topic**:
```shell
docker exec mosquitto mosquitto_sub -h 127.0.0.1 -t test
```

### Testing with Postgres in docker

You may need this setup to test:

* Recommendation Service

#### Setup

CSV files are available in the [../training-with-artificial-data/data_0409_0/data4db/](../training-with-artificial-data/data_0409_0/data4db/) path.

To **run the container**:

Go to `training-with-artificial-data/data_0419_0/data4db` and run

```shell
docker run -v $PWD:/usr/local/pgsql/data -e POSTGRES_PASSWORD=root -p 5432:5432 -d postgres
```

To **create a tables**:

Install postgresql client. If you are using Ubuntu, you can use the command

```shell
sudo apt-get install postgresql
```

Connect to the database using

```shell
psql -h 127.0.0.1 -p 5432 -U postgres
```

Create tables

```sql
CREATE TABLE coupon_info (
  coupon_id INT,
  coupon_type VARCHAR(16),
  department VARCHAR(10),
  discount INT,
  how_many_products_required INT,
  start_date VARCHAR(10),
  end_date VARCHAR(10),
  product_mean_price REAL,
  products_available INT,
  PRIMARY KEY (coupon_id)
);

CREATE TABLE product_info (
    product_id INT,
    name VARCHAR(256),
    category VARCHAR(50),
    sizes VARCHAR(50),
    vendor VARCHAR(50),
    description VARCHAR(256),
    buy_price REAL,
    department VARCHAR(10),
    PRIMARY KEY (product_id)
);

CREATE TABLE coupon_product (
    coupon_id INT,
    product_id INT,
    FOREIGN KEY (coupon_id) REFERENCES coupon_info(coupon_id),
    FOREIGN KEY (product_id) REFERENCES product_info(product_id)
);

CREATE TABLE customer_info (
  customer_id INT,
  gender VARCHAR(1),
  age INT,
  mean_buy_price REAL,
  total_coupons_used INT,
  mean_discount_received REAL,
  unique_products_bought INT,
  unique_products_bought_with_coupons INT,
  total_items_bought INT, 
  PRIMARY KEY (customer_id)
);
```

You could use the data prepared with [training-with-artificial-data](training-with-artificial-data) project.

There is a pregenerated data set (csv files) accompanied by python scripts to create the tables and load it into
the database in the [cachedb-load-data](cachedb-load-data) directory. The [README doc](cachedb-load-data/README.md) 
file contains usage information (including instruction for running the scripts in a docker container).
