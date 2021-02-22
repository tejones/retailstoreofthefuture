import json
import logging


class JsonExp():
    @staticmethod
    def export(path, filename='json.json', indent=None, **keys):
        logger = logging.getLogger('datagen')
        logger.debug(f"Exporting data to JSON {filename}")
        with open(f"{path}/{filename}", 'w') as f:
            json.dump(keys, f, indent=indent)
