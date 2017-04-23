import logging
from time import time


class Timer:
    """
    A class to investigate code runtime.
    """
    def __init__(self, seed):
        """
        Timer Initialisation
        :param seed: The seed of the world being timed
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        path = r'log/%s.log' % seed
        open(path, 'w').close()

        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.previous_time = time()

    def take_time(self, msg='', *args):
        current_time = time()
        self.logger.info('%s: %f', msg, current_time - self.previous_time)
        self.previous_time = current_time

        if args:
            self.logger.info('----------------%s----------------' % ', '.join(map(str, args)))
