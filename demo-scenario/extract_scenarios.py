import json
import os

from config import SCENARIOS_PATH


class NoValidScenariosFound(Exception):
    pass


def get_all_files(path: str) -> list:
    print(f'Looking for files in {path}...')
    files = []
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        print(f"Path {path} does not exist.")
        exit(1)
    print(f"Found {len(files)} files.")
    return ['/'.join([path, file]) for file in files]


def extract_scenarios():
    scenarios = []

    files = get_all_files(SCENARIOS_PATH)

    for file in files:
        try:
            with open(file) as f:
                scenarios.append(json.load(f))
        except json.JSONDecodeError:
            print(f"File {file} is not a valid JSON file.")
            print(f"!!! Skipping {file}", '!' * 20, end=' ')
            continue

    if not scenarios:
        raise NoValidScenariosFound

    return scenarios
