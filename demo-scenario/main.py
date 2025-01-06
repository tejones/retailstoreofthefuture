import paho.mqtt.client as mqtt
import json
import time

from extract_scenarios import extract_scenarios, NoValidScenariosFound
from config import MQTT_TOPICS, MQTT_HOST, MQTT_PORT, STEP_LENGTH


def send_mqtt_message(client: mqtt, topic: str, message: str) -> None:
    print(f"Sending message to topic {topic}: {message}")
    client.publish(topic, message)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT)

    steps = 0
    scenarios = []

    try:
        scenarios = extract_scenarios()
    except NoValidScenariosFound:
        print("No valid scenarios found. Exiting.")
        exit(1)

    # Find the longest scenario
    for scenario in scenarios:
        if len(scenario) >= steps:
            steps = len(scenario)

    # Send steps (messages) in a loop
    for step in range(steps):
        for scenario in scenarios:
            if len(scenario) > step:
                event = scenario[step]

                if event['type'] is None:
                    continue

                topic = MQTT_TOPICS[event['type']]
                message = event['message']
                message['ts'] = time.time()

                send_mqtt_message(client, topic, json.dumps(message))

        time.sleep(STEP_LENGTH)

    client.disconnect()
    print("Simulation finished.")
