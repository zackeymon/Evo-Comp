
import logging
from time import time


class Timer:
    def __init__(self, seed):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        path = r'log/%s.log' % seed
        open(path, 'w').close()

        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.previous_time = time()

    def take_time(self, msg='', end_day=False):
        current_time = time()
        self.logger.info('%s: %f', msg, current_time - self.previous_time)
        self.previous_time = current_time

        if end_day:
            self.logger.info('----------------END DAY----------------')
