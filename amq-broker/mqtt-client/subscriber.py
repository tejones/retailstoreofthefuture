import paho.mqtt.client as mqtt

TOPIC_NAME = "TestTopic"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(TOPIC_NAME)  

def on_message(client, userdata, msg):
    print(msg.topic + ": "+ str(msg.payload))

client = mqtt.Client()
client.username_pw_set("admin", "admin")
client.tls_set("certs/broker.pem")
client.tls_insecure_set(True) # disable hostname verification

client.on_connect=on_connect
client.on_message = on_message

client.connect("ex-aao-mqtt-2-svc-rte-pkolakow.apps.red.ocp.public", 443, 60)
client.loop_forever()
