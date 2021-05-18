# Functionality 
This service creates MQTT consumers to listen to "entry event" and "focus event".

**Entry event** is generated (externally), whenever a customer enters the store.

**Focus event** is generated (externally), whenever the platform detects, that a customer has stopped in a given
department (he is probably interested in buying some goods from that department).

This service's responsibility is to:

* fetch customer context (purchase history, demographics, etc.) from "the central" (datacenter), when the service
  receives *entry event*
* invoke/call prediction service to decide if the customer is willing to use promotion coupons from given department,
  when the service receives *focus event* and send prediction result to a dedicated MQTT topic.

## Table of contents

* [Functionality](#functionality)
  * [Event payloads](#event-payloads)
    * [Entry Event](#entry-event)
    * [Focus Event](#focus-event)
    * [Prediction Results Message](#prediction-results-message)
  * [Prediction request](#prediction-request)
* [Development](#development)
  * [Dependencies](#dependencies)
  * [Service configuration](#service-configuration)
  * [Running the service](#running-the-service)
  * [Testing without MQTT](#testing-without-mqtt)
  * [Docker image](#docker-image)
  * [Mock event endpoints](#mock-event-endpoints)
  * [Cache - DB](#cache---db)

## Event payloads

The service assumes the following data will be provided with given event types (using MQTT).

### Entry Event

The service listens for MQTT messages.

Topic: configurable - `ENTRY_EVENT_TOPIC_NAME` environment variable

Payload:

```
JSON

{
  "id": string,
  "ts": int
}
```

Example payload:
```json
{
  "id": "127",
  "ts": 192322800
}
```

### Focus Event

The service listens for MQTT messages.

Topic: configurable - `FOCUS_EVENT_TOPIC_NAME` environment variable

Payload:

```
JSON

{
  "id": string,             # Customer ID
  "ts": int,                # Timestamp (unix time)
  "dep": string,            # Department name
  "x": Optional[int],       # X coordinate of the event; optional
  "y": Optional[int]        # Y coodrinate of the event; optional
}
```

Payload example:

```json
{
  "id": "127",
  "ts": 192322800,
  "dep": "Boys"
}
```

ATTOW, supported categories are 'Boys', 'Girls', 'Men', 'Sports', 'Women'.

### Prediction Results Message

The service produces MQTT messages with the prediction.

Topic: configurable - `COUPON_PREDICTION_TOPIC_NAME` environment variable

Payload:

```
JSON

{
  "customer": {
    "id": string            # Customer ID
  },
  "coupon": {
    "id": int   ,           # Coupon ID
    "type": string,         # Coupon type (one of: "buy_more", "buy_all", "just_discount", "department")
    "department": string,   # Department name (supported categories are: 'Boys', 'Girls', 'Men', 'Sports', 'Women')
    "discount": float,      # Coupon discount in percentage
    "how_many": int,        # How many items must be bought to recieve a discount, depents on the type
                            #   buy_more: how many items of the same product must be bought
                            #   buy_all: the number of products to buy - all from the list must be bought
                            #   just_discount: always 1
                            #   department: always -1
    "start_date": string,   # Coupon valid from date
    "end_date": string,     # Coupon valid to date
    "products": [{          # List of products covered by the coupon
      "id": int,            # Product id
      "name": string,       # Product name
      "category": string,   # Product category
      "sizes": string,      # Available sizes
      "vendor": string,     # Vendor
      "description": str,   # Item description
      "buy_price": float,   # Regular item price
      "department": str     # Product department
    }]
  },
  "ts": int                 # Timestamp (unix time)
}
```

Payload example:

```json
{
  "customer": {
    "id": "11"
  },
  "coupon": {
    "id": "22",
    "type": "buy_more",
    "department": "Men",
    "discount": 14.0,
    "how_many": 3,
    "start_date": "2010-01-01",
    "end_date": "2010-01-01",
    "products": [{
      "id": "33",
      "name": "NGESNEALAND - Deep taupe Denim cut-offs for Women",
      "category": "Denim cut-offs",
      "sizes": "S-XL",
      "vendor": "TinyCottons",
      "description": "NGESNEALAND - Deep...",
      "buy_price": 7.12,
      "department": "Women"
    }]
  },
  "ts": 192322800
}
```

## Prediction request 
In order to do the actual prediction, a REST call is made.

**TBD**
(See: [prediction.schema.json](schema/prediction.schema.json))


# Development

## Dependencies

Dependencies of the project are contained in [requirements.txt](requirements.txt) file. All the packages are publicly
available.

All the packages can be installed with:
`pip install -r requirements.txt`

## Service configuration

The service reads the following **environment variables**:

| Variable               | Description                             |  Default      |
|------------------------|-----------------------------------------|--------------:|
| MQTT_HOST              | comma-separated list of MQTT brokers    |    	    	 - |
| MQTT_PORT              | MQTT brokers' port                      |    	    	 - |
| MQTT_USERNAME          | MQTT user username                      | None              |
| MQTT_PASSWORD          | MQTT user password                      | None              |
| MQTT_BROKER_CERT_FILE  | path to MQTT ssl cert file              | None              |
| ENTRY_EVENT_TOPIC_NAME | topic for entry events              	   |    	    	 - |
| FOCUS_EVENT_TOPIC_NAME | topic for focus events              	   |    	    	 - |
| COUPON_PREDICTION_TOPIC_NAME | topic for sending prediction results |   	   	 - |

(Parameters with `-` in "Default" column are required.)

Use [log_config.py](./app/utils/log_config.py) to **configure logging behaviour**. 
By default, console and file handlers are used. The file appender writes to `messages.log`.


## Running the service

For my development I created a project with dedicated virtual environment (Python 3.8, all the dependencies installed
there).

The code reads sensitive information (tokens, secrets) from environment variables. They need to be set accordingly in
advance.
`.environment.variables.sh` can be used for that purpose. Then, in order to run the service the following commands can be
used:

```
$ . .environment.variables.sh
$ . venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload --reload-dir app
```
> Please, note `reload-dir` switch. Without it the reloader goes into an infinite loop because it detects log file changes (messages.log).


## Testing without MQTT
For testing purposes, there are two endpoints that simulate events ("entry event", "focus event"),
as if they would appear on a dedicated MQTT topic.

In order for the service not to create real MQTT consumers and producers,
set `TESTING_NO_MQTT` environment variable to "true".

This way, event processing logic can be tested without MQTT, for example:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mock_entry' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"id": "127", "ts": 192322800}'
```

or:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mock_focus' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"id": "127", "ts": 192322800, "dep": "Boys"}'
```

## Docker image
The docker image for the service is [Dockerfile](Dockerfile).
It is based on FastAPI "official" image. 
See https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker 
for detail on configuring the container (http port, log level, etc.)

In order to build the image use:
```
docker build -t recommendation-service:0.0.1 .
```

> Set image name (`recommendation-service`) and tag (`0.0.1`) according to
> your needs.

To run the service as a Docker container run:
```
docker run -d -e LOG_LEVEL="warning"  --name recommendaition-service recommendation-service:0.0.1

```

## Mock event endpoints
For testing purposes, there are two endpoints that simulate events ("entry event", "focus event"),
as if they would appear on dedicated MQTT topic.

This way, event processing logic can be tested without MQTT, for example:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mock_entry' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_type": "entry event",
  "event_timestamp": "2021-03-18T08:29:02.160Z",
  "payload": {
    "customer_id": 3
  }
}'
```
or:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/mock_focus' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_type": "focus event",
  "event_timestamp": "2021-03-18T08:29:02.160Z",
  "payload": {
    "customer_id": 8,
    "category": "Women" 
  }
}'
```

## Cache - DB

This component uses PostgreSQL as a cache. It stores coupons and customer data.

DB tables:

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

CREATE_TABLE product_info (
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

CREATE_TABLE coupon_product (
    coupon_id INT,
    product_id INT,
    FOREIGN KEY (coupon_id) REFERENCES coupon_info(coupon_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)

CREATE TABLE customer_info (
  ustomer_id INT,
  gender VARCHAR(1),
  age INT,
  mean_buy_price REAL,
  total_coupons_used: INT,
  mean_discount_received: REAL,
  unique_products_bought INT,
  unique_products_bought_with_coupons: INT,
  total_items_bought:
  INT, PRIMARY KEY (customer_id)
);
```

How to fill DB with data:

```sql
COPY coupon_info FROM '<<DATA_PATH>>/coupon_info.csv' DELIMITER ',' CSV HEADER;
COPY product_info FROM '<<DATA_PATH>>/products.csv' DELIMITER ',' CSV HEADER;
COPY coupon_product FROM '<<DATA_PATH>>/coupon_product.csv' DELIMITER ',' CSV HEADER;
COPY customer_info FROM '<<DATA_PATH>>/customer_info.csv' DELIMITER ',' CSV HEADER;
```

CSV files are available in the [../training-with-artificial-data/data_0409_0/data4db/](../training-with-artificial-data/data_0409_0/data4db/) path
