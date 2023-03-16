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

## Service configuration

The service reads the following **environment variables**:

| Variable                | Description                          | Default |
|-------------------------|--------------------------------------|--------:|
| MQTT_HOST               | comma-separated list of MQTT brokers |       - |
| MQTT_PORT               | MQTT brokers' port                   |    	  - |
| MQTT_USERNAME           | MQTT user username                   |    None |
| MQTT_PASSWORD           | MQTT user password                   |    None |
| MQTT_BROKER_CERT_FILE   | path to MQTT ssl cert file           |    None |
| FOCUS_TOPIC             | topic for focus events               |    	  - |
| PERIODIC_TASKS_INTERVAL | repeat publication every n seconds   |    	  1 |
| GENERATOR_AUTO_START    | start generating when the app starts |    True |
| LOG_LEVEL               | logging level                        |    INFO |

(Parameters with `-` in the "Default" column are required.)

Use [log_config.py](./app/utils/log_config.py) to **configure logging behaviour**. 
By default, console and file handlers are used. The file appender writes to `messages.log`.

## Running the service

For development, I created a project with a dedicated virtual environment (Python 3.8, all the dependencies installed
there).

The code reads sensitive information (tokens, secrets) from environment variables. They need to be set accordingly in
advance.
`.environment.variables.sh` can be used for that purpose. Then, in order to run the service the following commands can be
used:

```bash
$ . .environment.variables.sh
$ . venv/bin/activate
(venv)$ uvicorn app.main:app --host 0.0.0.0 --reload --reload-dir app
```
> Please, note `reload-dir` switch. Without it the reloader goes into an infinite loop because it detects log file changes (messages.log).

## Testing without MQTT
For testing/development purposes, you can use a dummy MQTT client that does not connect to a real broker.

In order for the service not to create real MQTT producers, set `TESTING_NO_MQTT` environment variable to "true".


## TODO
* Describe the service's API (http)
* Dockerize the service
