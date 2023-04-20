import os
import paho.mqtt.client as mqtt
import time

SLEEP_TIME=1
host = os.environ.get('HTTP_HOST', 'localhost')
port = int(os.environ.get('HTTP_PORT', 1883))


def on_publish(client, userdata, result):
    print("Published")

client = mqtt.Client()
client.on_publish = on_publish
client.connect(host, port)
client.loop_start()


i = 0
while True:
    client.publish("test", f"Message {i}")
    i += 1
    time.sleep(SLEEP_TIME)
