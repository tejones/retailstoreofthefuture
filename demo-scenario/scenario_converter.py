import json
import os

from config import SCENARIOS_PATH


try:
    STEPS_DELAY = int(os.getenv('STEPS_DELAY', 0))
except ValueError:
    print("STEPS_DELAY must be an integer.")
    exit(1)


try:
    SCENARIO = json.loads(os.getenv('SCENARIO'))   # format of scenario generator in the UI (check README.md)
except KeyError:
    print("Please provide SCENARIO environment variable.")
    exit(1)
except json.JSONDecodeError:
    print("Please provide valid JSON in SCENARIO environment variable.")
    exit(1)


class ScenarioStructureInvalid(Exception):
    pass


def change_structure(data: dict, cid: int) -> dict:
    try:
        new_structure = {
            'type': data['type'],
            'message': {
                'id': cid,
                'x': data['location']['x'],
                'y': data['location']['y']
            }
        }
    except KeyError:
        raise ScenarioStructureInvalid
    return new_structure


if __name__ == "__main__":
    cid = SCENARIO['customer']['customer_id']
    events = [{"type": None} for _ in range(STEPS_DELAY)]

    try:
        for event in SCENARIO['path']:
            new_event = change_structure(event, cid)
            events.append(new_event)
    except ScenarioStructureInvalid:
        print (f"Given scenario has wrong structure. Check the README.md file.")
        exit(1)

    f_name = f'{SCENARIOS_PATH}/scenario_{cid}.json'

    if os.path.exists(f_name):
        print(f"File {f_name} already exists. Exiting.")
        exit(1)

    with open(f_name, 'w') as f:
        json.dump(events, f, indent=4)
    