# Scenario Player

This project was a part of a broader demo. That broader demo analyzed customers' movement in a retail store, determined
their behavior (for example: "customer stopped in men's clothes department"), and use Machine Learning to model for
purchase/product recommendation. The customer location was determined by movement sensors placed in the store.

This service simulates customer behavior in a retail shop:

* customer entering the store
* customer movement
* customer exiting the store

by generating proper MQTT messages.

## Table of contents

* [Usage](#usage)
  * [Main simulator loop](#main-simulator-loop)
  * [Scenario definitions](#scenario-definitions)
  * [Messages payloads](#messages-payloads)
* [Running the service](#running-the-service)
* [Development information](#development-information)

# Usage

This is a web service (implemented with FastAPI). By default, it works on port 8000.
(See [instructions](./development.md#running-the-service) for details on configuring and running the service.)

When starting, it does the following:

* connects to MQTT server
* waits for and registers new user movement scenarios (HTTP POST to `/scenario` endpoint)
* creates a background task (ran every second) that checks if there is something to be sent (if it is time for giving an
  update on the particular customer)

## Main simulator loop
The main loop executes every second and tries to locate events (in the timeline) that should be 
"replayed". If there are any, proper messages are constructed and published (via. `Publisher` object).

> Please, note, that in the current implementation, the main simulator loop replays
> events from the timeline for **current timestamp** (current date/time).

## Scenario definitions

The scenario is a list of locations for a given customer in certain moments, for example: 

```json
{
  "customer": {
    "customer_id": "3"
  },
  "path": [
    {
      "type": "ENTER",
      "location": {"x": 200, "y": 10},
      "timestamp": "2021-04-11T10:01:53.955760"
    },
    {
      "type": "MOVE",
      "location": {"x": 320, "y": 150},
      "timestamp": "2021-04-11T10:13:49.614897"
    },
    {
      "type": "EXIT",
      "location": {"x": 200, "y": 10},
      "timestamp": "2021-04-11T12:31:17.437862"
    }
  ]
}
```

The service can register a scenario:

```shell
curl -X 'POST' \
  'http://localhost:8000/scenario' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"customer":{"customer_id":"1"},"path":[{"type":"ENTER","location":{"x":935,"y":50},"timestamp":1618323771180},{"type":"MOVE","location":{"x":588.9128630705394,"y":454.08039288409145},"timestamp":1618323772180},{"type":"EXIT","location":{"x":1075,"y":50},"timestamp":1618323773180}]}'
```

After receiving the request, the service adds all steps (from `path`) to the current timeline
with timestamps as defined in the payload.

As the main loop uses the current timestamp for "locating" the events on the timeline, 
it is possible that registered events won't ever be published. 
In case the timestamp of a given event _is in the past_, it will be never be retrieved and processed.


For user convenience, it is possible to reuse a scenario definition that refers to the past.
`recalculate_time=true` parameter for `/scenario` request can be used here:

```shell
curl -X 'POST' \
  'http://localhost:8000/scenario?recalculate_time=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"customer":{"customer_id":"1"},"path":[{"type":"ENTER","location":{"x":935,"y":50},"timestamp":1618323771180},{"type":"MOVE","location":{"x":588.9128630705394,"y":454.08039288409145},"timestamp":1618323772180},{"type":"EXIT","location":{"x":1075,"y":50},"timestamp":1618323773180}]}'
```

In this case, the scenario will start with the current time and step timestamps will be recalculated appropriately
(they will be "refreshed").

## Messages payloads

### **customer/exit** Channel

| Name | Type    | Description                                    | Accepted values |
|------|---------|------------------------------------------------|-----------------|
| id   | string  | ID of the customer                             | ...             |
| ts   | integer | Timestamp of the event, in seconds since epoch | ...             |

Example of payload:

```json
{
  "id": "127",
  "ts": 192322800
}
```

### **customer/exit** Channel

| Name | Type    | Description           | Accepted values |
|------|---------|-----------------------|-----------------|
| id   | string  | ID of the customer    | ...             |
| ts   | integer | Timestamp (unix time) | ...             |

Example of payload:

```json
{
  "id": "127",
  "ts": 192322800
}
```

### **customer/move** Channel

| Name | Type    | Description           | Accepted values |
|------|---------|-----------------------|-----------------|
| id   | string  | ID of the customer    | ...             |
| ts   | integer | Timestamp (unix time) | ...             |
| x    | integer | coordinate x          | ...             |
| y    | integer | coordinate y          | ...             |

Example of payload:

```json
{
  "id": "127",
  "ts": 192322800,
  "x": 0,
  "y": 0
}
```

# Running the service
See [instructions](./development.md#running-the-service) for details on configuring and running the service locally.

# Development information
See [development.md](./development.md) for information about configuring the service, how to run test and run the
service.
