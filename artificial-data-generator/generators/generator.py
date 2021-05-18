from abc import abstractmethod, ABC
import logging


class Generator(ABC):
    def __init__(self):
        self.logger = logging.getLogger('datagen')

    @abstractmethod
    def generate(self):
        pass
