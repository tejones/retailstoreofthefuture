## Functionality
This service generates messages that simulate customer behavior in a retail shop:
* customer entering the store
* customer movement 
* customer exiting the store

## Table of contents
* [Development](#development)
  * [Dependencies](#dependencies)
  * [Service configuration](#service-configuration)
  * [Running the service](#running-the-service)
  * [Testing with MQTT broker in docker](#testing-with-mqtt-broker-in-docker)
  * [Testing without MQTT](#testing-without-mqtt)
  * [Mock event endpoints](#mock-event-endpoints)
* [Deployment](#deployment)
  * [Docker image](#docker-image)
  * [Connecting to a secured broker](#connecting-to-a-secured-broker)

## Development

### Dependencies

Dependencies of the project are contained in [requirements.txt](requirements.txt) file. All the packages are publicly
available.

All the packages can be installed with:
`pip install -f requirements.txt`

### Service configuration

The service reads the following **environment variables**:

| Variable                   | Description                                 |        Default |
|----------------------------|---------------------------------------------|---------------:|
| STORE_HEIGHT               | Unused                                      |             10 |
| STORE_WIDTH                | Unused                                      |              6 |
| CUSTOMERS_AVERAGE_IN_STORE | Unused                                      |              6 |
| CUSTOMERS_LIST_FILE        | Unused                                      |  customers.csv |
| MQTT_HOST                  |                                             |              - |
| MQTT_PORT                  |                                             |           1883 |
| MQTT_CLIENT_ID             |                                             |     demoClient |
| ENTER_TOPIC                |                                             | customer/enter |
| MOVE_TOPIC                 |                                             |  customer/move |
| EXIT_TOPIC                 |                                             |  customer/exit |
| LOG_LEVEL                  | logging level                               |           INFO |
| LOG_FILENAME               | log file name                               |             '' |
| CONSUME_FREQUENCY          | how often check the timeline for events [s] |            1.0 |
| CONSUME_FROM               | from when start getting events (see below)  |         latest |
| CONSUME_BATCH_SIZE         | how many events to take at once             |             10 |

(Parameters with `-` in the "Default" column are required.)

Use env variables [log_config.py](./app/log_config.py) to **configure logging behaviour**.
By default, console is used for logging. File handler is added if `LOG_FILENAME` is provided.

Some of the parameters are explained in more detail below.

**CONSUME_FROM** - where to start consuming messages from.
When the service starts, it needs to know where to start consuming messages from.
It can be either:
* `earliest`
* `latest`
* specific point in time (ISO 8601 format)

When `earliest` is used, the service will start consuming messages from the beginning of the timeline.

When `latest` is used, the service will start consuming messages from the point of time, when it was started.

When specific point in time is used, the service will start consuming messages from the first message
that has timestamp greater than or equal to the specified point in time.

**CONSUME_FREQUENCY** - how often check the timeline for events.
The service keeps a timeline of
events (customer entering, moving, exiting) -- it keeps track of the time of the specific events to occur.
Then the service checks if there are any events to be published at the current time.
The checking is done periodically (controlled by `CONSUME_FREQUENCY` parameter).
It happens every `CONSUME_FREQUENCY` seconds.
A higher frequency can help generate greater traffic and facilitate horizontal scaling of the service.

**CONSUME_BATCH_SIZE** - how many events from the timeline to take in one go.
smaller batch size can provide more fine-grained control over resource consumption and processing latency.
Like CONSUME_FREQUENCY, CONSUME_BATCH_SIZE can also play a role in horizontal scaling by enabling the system to process more data in parallel.


### Running the service

For development, I created a project with a dedicated virtual environment (Python 3.8, all the dependencies installed
there).

The code reads sensitive information (tokens, secrets) from environment variables. They need to be set accordingly in
advance.
`environment.variables.sh` can be used for that purpose. Then, in order to run the service the following commands can be
used:

```shell
$ . .environment.variables.sh
$ . venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload --reload-dir app
```

> Please, note `reload-dir` switch. Without it the reloader goes into an infinite loop because it detects log file changes (messages.log).

### Testing with MQTT broker in docker

[Check DEPLOYMENT tips](../DEPLOYMENT.md) to find out how to deploy and use the MQTT service for development purposes.

### Testing without MQTT
There is an environment variable, `TESTING_MOCK_MQTT`, that will create an MQTT client mock instead of trying to connect
to a real MQTT broker. Instead of publishing the messages, they will be simply logged/printed out.

This may be helpful for local development or testing.

#### Producing test messages

```shell
curl http://127.0.0.1:8000/produce_entry -d '{"id": "997", "ts": 192326400}'
```

```shell
curl http://127.0.0.1:8000/produce_exit -d '{"id": "997", "ts": 192326400}'
```

```shell
curl http://127.0.0.1:8000/produce_move -d '{"id": "997", "ts": 192326400, "x": 2, "y": 3}'
```

## Deployment

### Docker image
The docker image for the service is [Dockerfile](Dockerfile).
In order to build the image use:

```shell
docker build -t customersim-service:0.0.1 .
```

> Set image name (`customersim-service`) and tag (`0.0.1`) according to your needs.

To run the service as a Docker container run:

```shell
docker run -d -e LOG_LEVEL="warning"  --name customersim-service customersim-service:0.0.1
```

### Connecting to a secured broker
**TODO** Add info about setting user/password
**TODO** Add info about using client certificates (TLS)
