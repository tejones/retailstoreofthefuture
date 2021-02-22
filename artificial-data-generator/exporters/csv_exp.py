import csv
import logging


class CsvExp:
    @staticmethod
    def export(path, filename='csv.csv', data=None):
        logger = logging.getLogger('datagen')
        logger.debug(f"Exporting data to CSV {filename}")
        if data is None or len(data) == 0:
            raise Exception('Put some data')

        keys = data[0].keys()

        with open(f"{path}/{filename}", 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
