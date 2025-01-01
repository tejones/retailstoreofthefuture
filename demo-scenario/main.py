import paho.mqtt.client as mqtt
import json
import time

from scenarios import SCENARIOS

BROKER = "localhost"
PORT = 1883

TOPICS = {
    'MOVE': 'customer/move',
    'ENTER': 'customer/enter',
    'EXIT': 'customer/exit',
    'BROWSING': 'customer/browsing',
    'PREDICTION': 'customer/prediction'
}


def send_mqtt_message(client, topic, message):
    print(f"Sending message to topic {topic}: {message}")
    client.publish(topic, message)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(BROKER, PORT)

    steps = 0

    for scenario in SCENARIOS:
        if len(scenario) >= steps:
            steps = len(scenario)

    for step in range(steps):
        for scenario in SCENARIOS:
            if len(scenario) > step:
                event = scenario[step]

                if event['type'] is None:
                    continue

                topic = TOPICS[event['type']]
                message = event['message']
                message['ts'] = time.time()

                send_mqtt_message(client, topic, json.dumps(message))

        time.sleep(1)

    client.disconnect()