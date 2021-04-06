# Functionality 
This service generates messages that simulate customer behaviour in a reatail shop:
* customer entering the store
* customer movement 
* customer exiting the store


## Table of contents
* [Functionality](#functionality)
* [Event payloads](#event-payloads)
    * [customer/enter](#customerenter)
    * [customer/move](#customermove)
    * [customer/exit](#customerexit)

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



## Event payloads
The service assumes the following data will be provided with given event types.

This script generates the following MQTT messages

### customer/enter

```
{ 
  id: --ID representing customer--, 
  ts: --timestamp of the entrance, in seconds since epoch-- 
}
```

### customer/move

```
{ 
 id: --ID representing customer--,
 ts: --timestamp of the move, in seconds since epoch--,
  x: --x coordinate of location sensor that fired--,
  y: --y coordinate of location sensor that fired--
}
```

### customer/exit

```
{ 
 id: --ID representing customer--,
 ts: --timestamp of the exit, in seconds since epoch--
}
```



# Development

## Dependencies

Dependencies of the project are contained in [requirements.txt](requirements.txt) file. All the packages are publicly
available.

All the packages can be installed with:
`pip install -f requirements.txt`

## Service configuration

The service reads the following **environment variables**:

| Variable               | Description                          |  Default      |
|------------------------|--------------------------------------|--------------:|
| STORE_HEIGHT          |                                       | 10            |
| STORE_WIDTH           |                                       | 6             |
| CUSTOMERS_AVERAGE_IN_STORE |  					            | 6 		    |
| CUSTOMERS_LIST_FILE   |                                       | customers.csv |
| MQTT_HOST             |                                       | -             |
| MQTT_PORT             |               	                    | 1883          |
| MQTT_NAME             |                	                    | demoClient    |
| ENTER_TOPIC           |                                       | customer/enter|
| MOVE_TOPIC            |                                       | customer/move |
| EXIT_TOPIC            |                                       | customer/exit |

(Parameters with `-` in "Default" column are required.)

Use [log_config.py](./app/utils/log_config.py) to **configure logging behaviour**. 
By default, console and file handlers are used. The file appender writes to `messages.log`.


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
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload --reload-dir app
```
> Please, note `reload-dir` switch. Without it the reloader goes into an infinite loop because it detects log file changes (messages.log).

## Testing with MQTT broker in docker

Quick way to **set up a simple MQTT broker** is to use Docker containers:
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

### Testing without MQTT
There is an environment variable, `TESTING_MOCK_MQTT`, that will create an MQTT client mock instead of trying to connect
to a real MQTT broker. Instead of publishing the messages, they will be simply logged/printed out.

This may be helpful for local development or testing.

### Producing test messages

```shell
curl http://127.0.0.1:8000/produce_entry -d '{"id": "997", "ts": 192326400}'
 ```

```shell
curl http://127.0.0.1:8000/produce_exit -d '{"id": "997", "ts": 192326400}'
 ```

```shell
curl http://127.0.0.1:8000/produce_move -d '{"id": "997", "ts": 192326400, "x": 2, "y": 3}'
 ```


# Deployment

## Docker image
The docker image for the service is [Dockerfile](Dockerfile).
It is based on FastAPI "official" image.
See https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
for the details on configuring the container (http port, log level, etc.)

In order to build the image use:
```
docker build -t customersim-service:0.0.1 .
```

> Set image name (`customersim-service`) and tag (`0.0.1`) according to
> your needs.

To run the service as a Docker container run:
```
docker run -d -e LOG_LEVEL="warning"  --name customersim-service customersim-service:0.0.1

```

## Connecting to a secured broker
**TODO** Add info about setting user/password
**TODO** Add info about using client certificates (TLS)
