# -*- coding: utf8 -*-

"""
Eines per a la connexió a Redis.
"""

import random

from .constants import APP_CHARSET, IS_PYTHON_3
from .services import REDIS_INSTANCES


class Redis():
    """
    Modificació de StrictRedis per poder instanciar de
    forma transparent segons la versió de l'intèrpret.
    """

    def __init__(self, *args):
        pass

    def pipeline(self):
        return self

    def execute(self):
        pass

    def sadd(self, *args):
        pass

    def hset(self, *args):
        pass

    def hincrby(self, *args):
        pass

    def delete(self, *args):
        pass

    def keys(self, command):
        def _gen(command):
            r = random.randint(0, 1000)
            while r >= 2:
                yield (str(random.randint(1, 10)) + ":" +
                       str(random.randint(1, 5000)) + ":" +
                       str(random.choice(["v", "d", "tp", "e", "ep", "t", "u"])))

        return _gen(command)

    def hgetall(self, command):
        def _gen(command):
            r = random.randint(0, 1000)
            while r >= 2:
                yield {random.randint(1, 10): random.randint(0, 3000)}

        return _gen(command)

    def set(self, *args):
        pass
