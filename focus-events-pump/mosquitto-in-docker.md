Run vanilla mosquitto in docker:
```bash
docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto 
```

Running the broker with websockets on, persistence and proper listener configuration (port 1883) requires config like:
```
# mosquitto.conf file
listener 1883

listener 9001
protocol websockets

allow_anonymous true
persistence true
persistence_location /mosquitto/data

# log_dest file /mosquitto/log/mosquitto.log
log_dest stdout
log_dest topic
connection_messages true

```

```bash
docker run -it -p 1883:1883 -p 9001:9001 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto
```

The same, but non-interactive:
```bash
docker run --name mosquitto -d -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto
```


The client (sub):
```bash
docker run -it --net=host eclipse-mosquitto mosquitto_sub -h localhost -t example/topic
```



The client (pub):
```bash

docker run -it --net=host eclipse-mosquitto mosquitto_pub -h localhost -t example/topic -m "Hello World"
```

Publish 100 messages:
```bash
for i in {1..100}; do docker run -it --net=host eclipse-mosquitto mosquitto_pub -h localhost -t example/topic -m "Hello World $i"; done
```
