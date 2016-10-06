import string
import random
from django.conf import settings
from functools import lru_cache


sample = ''.join([string.ascii_lowercase,
                  string.ascii_uppercase,
                  string.digits,
                  '-'])


def randomstr(n=6):
    return ''.join(random.sample(sample, n))


@lru_cache()
def api_path(path):
    return ''.join([settings.BASE_URL, settings.TOKEN, '/', path.strip('/')])


def gen_delay(task):
    return random.triangular(1.1, 2.5, 2.1) ** task.request.retries


def dict_to_markdown(dikt, order=()):
    lines = []
    if not order:
        order = list(dikt.keys())
        order.sort()
        order = tuple(order)
    for o in order:
        if type(o) is tuple:
            key, text = o
        else:
            key, text = (o, o)
        value = dikt.get(key)
        if value:
            line = ''.join(['*', str(text), ':* ', str(value)])
            lines.append(line)

    return '\n'.join(lines)

