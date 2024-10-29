import os
import paho.mqtt.client as mqtt
import time

host = os.environ.get('HTTP_HOST', 'localhost')
port = int(os.environ.get('HTTP_PORT', 1883))
pid = os.getpid()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("$share/Group1/test")

def on_message(client, userdata, msg):
    print(f"[{pid}] Received: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()
