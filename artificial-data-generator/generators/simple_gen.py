from generators.generator import Generator
from generators.random_data_gen import RandomDataGen


class SimpleGen(Generator):
    def __init__(self, number_of_rows):
        self.number_of_rows = number_of_rows
        super().__init__()

    def generate(self):
        self.logger.debug('Generating Simple Data')
        rdg = RandomDataGen()
        items = []
        for i in range(1, self.number_of_rows + 1):
            items.append({
                'id': i,
                'name': rdg.generate_name_like_string()
            })

        return items