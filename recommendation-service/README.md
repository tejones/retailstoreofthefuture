
# Functionality 
This service creates Kafka consumers to listen to "entry event" and "focus event".

**Entry event** is generated (externally), whenever a customer enters the store.

**Focus event** is generated (externally), whenever the platform detects, that a customer has stopped in a given
department (he is probably interested in buying some goods from that department).

This service's responsibility is to:

* fetch customer context (purchase history, demographics, etc.) from "the central" (datacenter), when the service
  receives *entry event*
* invoke/call prediction service to decide if the customer is willing to use promotion coupons from given department,
  when the service receives *focus event* and send prediction result to a dedicated Kafka topic.

## Event payloads

The service assumes the following data will be provided with given event types.

### Entry Event
The schema for entry event payload is
![customer_entry schema](schema/customer_entry.png)

(See: [customer_entry.schema.json](schema/customer_entry.schema.json))

In this case, the example message looks like this:
```json
{
    "event_type": "customer entry",
    "event_timestamp": "2001-12-17T09:30:47.0",
    "payload": {
        "customer_id": 1
    }
}
```

### Focus Event
The schema for focus event payload is:
![customer_focus schema](schema/customer_focus.png)

(See: [customer_focus.schema.json](schema/customer_focus.schema.json))

In this case, the example message looks like this:

```json
{
    "event_type": "customer focus",
    "event_timestamp": "2001-12-17T09:30:47.0",
    "payload": {
        "customer_id": 1,
        "department_id": 1
    }
}
```

### Prediction Results Message
The schema for prediction result message is:
![prediction_result schema](schema/prediction_result.png)

(See: [prediction_result.schema.json](schema/prediction_result.schema.json))

In this case, the example message looks like this:

{
    "event_type": "prediction result",
    "event_timestamp": "2001-12-17T09:30:47.0",
    "payload": {
        "customer_id": 1,
        "coupon_id": 1,
        "prediction": 0.9
    }
}
## Prediction request 
In order to do the actual prediction, a REST call is made.

**TBD**
(See: [prediction.schema.json](schema/prediction.schema.json))


# Development

## Dependencies

Dependencies of the project are contained in [requirements.txt](requirements.txt) file. All the packages are publicly
available.

All the packages can be installed with:
`pip install -f requirements.txt`

## Service configuration

*TODO: explain the following parameters*

| Variable               | Description                             |  Default      |
|------------------------|-----------------------------------------|--------------:|
| BOOTSTRAP_SERVERS      | comma-separated list of Kafka brokers   | 127.0.0.1:9092|
| CLIENT_ID              | optional identifier of a Kafka consumer | kafkaClients  |
| GROUP_ID               | consumer group name 					   | None 		   |
| POLL_TIMEOUT           | time spent waiting for messages in in poll (ms) |   100 |
| AUTO_OFFSET_RESET      | see: auto.offset.reset setting in Kafka | 	  latest |
| ENTRY_EVENT_TOPIC_NAME | topic for entry events              	   |    		 - |
| FOCUS_EVENT_TOPIC_NAME | topic for focus events              	   |    		 - |
| COUPON_PREDICTION_TOPIC_NAME | topic for sending prediction results |   		 - |
| COUPON_SCORER_URL      | URL of the scorer service               |   			 - |


## Running the service

For my development I created a project with dedicated virtual environment (Python 3.8, all the dependencies installed
there).

The code reads sensitive information (tokens, secrets) from environment variables. They need to be set accordingly in
advance.
`environment.variables.sh` can be used for that purpose. Then, in order to run the service the following commands can be
used:

```
$ . .environment.variables.sh
$ . venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0
```

## Testing with Kafka in docker-compose

In my case, the quickest way to set up Kafka cluster for development purposes was to use Docker containers.

The procedure to **set up the cluster** boils down to:

```
curl --silent --output docker-compose.yml \
  https://raw.githubusercontent.com/confluentinc/cp-all-in-one/6.1.0-post/cp-all-in-one/docker-compose.yml

docker-compose up -d
```

See https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html for the details.

To **create a topic**:

```
docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic ENTRY_EVENT
```

where

* `broker` is the name of the container hosting Kafka broker instance
* `localhost:9092` is the broker's URL
* `ENTRY_EVENT` is the topic name

To **produce some testing messages**, one can issue the following command:

```
docker-compose exec broker  \
  bash -c "seq 10 | kafka-console-producer --request-required-acks 1 --broker-list localhost:9092 --topic ENTRY_EVENT && echo 'Produced 10 messages.'"
```

where

* `broker` is the name of the container hosting Kafka broker instance
* `ENTRY_EVENT` is the topic name
* `localhost:9092` is the broker's URL

