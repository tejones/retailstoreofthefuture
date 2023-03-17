# Focus Events Generator

This is a helper service that generates focus events (for the recommendation service)
and publishes them to an MQTT topic. The service is intended to be used for load testing Recommendation Service.

The topic and the frequency of events can be configured via environment variables.

The message payload is a JSON object with the following structure (see Recommendation Service project's README):

```json
{
  "id": "4",
  "dep": "Boys",
  "ts": 192322800
}
```

Please, note that this implementation is not universal. It is tailored to the needs of the
demo that uses predefined dataset (customers, coupons, etc.). The service assumes that the system operates on the same
dataset that CacheDB loader uses. (see: [CacheDB loader data](../cachedb-load-data/data))

Some of the characteristics of clients data are:
* there are 1000 clients
* ids of clients are integers from 1 to 1000

This allows for great simplifications -- instead of choosing from the actual set of clients' ids, the service can simply
generate random integers in the range [1, 1000].

Also, the generated message format is "static", not configurable. Which is enough for this simple purpose.


## Usage

This is a web service (implemented with FastAPI). By default, it works on port 8000.
(See [instructions](#running-the-service) for details on configuring and running the service.)

When starting, it does the following:

* connects to MQTT server
* creates a background task that periodically generates focus event payload and publishes it to MQTT topic

The message production starts automatically (when the service starts), unless `GENERATOR_AUTO_START` environment
variable is set to `False`.

Message publication can be paused and resumed by sending a POST request to `/stop` and `/start` endpoints respectively.

### HTTP endpoints

The service exposes the following HTTP endpoints:

| Method | Path         | Function                       |
|--------|--------------|--------------------------------|
| GET    | /healthcheck | can be used for liveness probe |
| POST   | /start       | start message publications     |
| POST   | /stop        | pause message publications     |

## Development

Dependencies of the project are contained in [requirements.txt](requirements.txt) file. All the packages are publicly
available.
For development, it may be convenient to have a dedicated virtual environment (Python 3.8+, all the dependencies
installed there).

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Service configuration

The service reads the following **environment variables**:

| Variable                | Description                          | Default |
|-------------------------|--------------------------------------|--------:|
| MQTT_HOST               | comma-separated list of MQTT brokers |       - |
| MQTT_PORT               | MQTT brokers' port                   |    	  - |
| MQTT_USERNAME           | MQTT user username                   |    None |
| MQTT_PASSWORD           | MQTT user password                   |    None |
| MQTT_BROKER_CERT_FILE   | path to MQTT ssl cert file           |    None |
| FOCUS_TOPIC             | topic for focus events               |       - |
| PERIODIC_TASKS_INTERVAL | repeat publication every n seconds   |       1 |
| GENERATOR_AUTO_START    | start generating when the app starts |    True |
| LOG_LEVEL               | logging level                        |    INFO |
| LOG_FILENAME            | log file name                        |      '' |

(Parameters with `-` in the "Default" column are required.)

Use env variables [log_config.py](./app/config/log_config.py) to **configure logging behaviour**.
By default, console is used for logging. File handler is added if `LOG_FILENAME` is provided.

## Running the service

The code reads sensitive information (tokens, secrets) from environment variables. They need to be set accordingly in
advance. `environment.variables.sh` can be used for that purpose. Then, in order to run the service the following
commands can be
used:

```shell
$ . .environment.variables.sh
$ . venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload --reload-dir app
```

> Please, note `reload-dir` switch. Without it the reloader goes into an infinite loop because it detects log file
> changes (messages.log).

## Testing without MQTT

For testing/development purposes, you can use a dummy MQTT client that does not connect to a real broker. 
Instead, it prints the messages to the console.

In order for the service not to create real MQTT producers, set `TESTING_NO_MQTT` environment variable to "true".

