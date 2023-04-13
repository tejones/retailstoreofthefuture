# Redis backend

Scenario Player is a service that simulates customer behavior in a retail shop. 

It can replay customer movement scenarios.
Those scenarios are defined in JSON format,
and can be submitted to the service via HTTP POST requests (`/scenario`, `/scenario_draft` endpoints).


Then the scenarios are persisted (in some [storage backend](app/backend/base.py)) and can be replayed by the service.

For basic usage (where there is no need to have great performance or scalability), the service can be run with the default
storage backend (which is simple in-memory storage, [PQueueTimelineBackend](app/backend/priority_queue.py),
based on a priority queue). The consequences of using this backend are:
* the scenarios are lost after the service is restarted
* every service instance holds its own timeline of events/steps which means that they cannot be shared between instances
  (e.g. to scale the service horizontally)

For more advanced use cases, the service can be run with a more sophisticated storage backend (e.g. Redis).
In this case, Redis holds the data for a timeline of events/steps (for all scenarios). 
Every Scenario Player service instance gets an exclusive event from the timeline
(the events are distributed across the instances of the Scenario Player) 
and processes it (sends a message to the MQTT server). This way, we can have multiple instances of the service
running in parallel and they can share the load.

Another advantage of using Redis backend is that the scenarios are persisted (in Redis) 
and can be replayed even after the service is restarted. 
In the case of the in-memory storage backend, the scenarios are lost after the service is restarted.

Summing up, Redis backend gives the following advantages:
* scenarios are persisted and can be replayed/continued after the service is restarted
* the service can be scaled horizontally (by running multiple instances of the service)
* there is better visibility of the data (e.g. the scenarios can be viewed in Redis CLI)


## Configuring the Redis backend
To use Redis backend, the following environment variables need to be set before running the service


| Variable name     | Description                            | Default value |
|-------------------|----------------------------------------|---------------|
| USE_REDIS_BACKEND | decide if redis backend should be used | false         |
| REDIS_HOST        | redis server host                      | -             |
| REDIS_PORT        | redis port                             | 6379          |
| REDIS_DB          | db number                              | 0             |
| REDIS_PASSWORD    | password used to connect to the server | ''            |

Values with `-` are required.
