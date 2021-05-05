import paho.mqtt.client as mqtt

TOPIC_NAME = "TestTopic"

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message Sent!")

client = mqtt.Client()
client.username_pw_set("admin", "admin")
client.tls_set("broker_cert.pem")
client.tls_insecure_set(True) # disable hostname verification
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("ex-aao-mqtt-0-svc-rte-pkolakow.apps.red.ocp.public", 443, 60)

message = "Test Message"
print(f"Sending mesasge to {TOPIC_NAME}: message")
client.publish(TOPIC_NAME,message)
