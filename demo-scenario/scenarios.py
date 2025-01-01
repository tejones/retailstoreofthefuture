import json

SCENARIOS = []

FILES = ['scenario_1.json', 'scenario_2.json', 'scenario_3.json']

for file in FILES:
    with open(file) as f:
        SCENARIOS.append(json.load(f))
