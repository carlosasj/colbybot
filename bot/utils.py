import string
import random
from django.conf import settings
from functools import lru_cache


sample = ''.join([string.ascii_lowercase, string.digits])


def randomstr(n=6):
    return ''.join(random.sample(sample, n))


@lru_cache()
def api_path(path):
    return ''.join([settings.BASE_URL, settings.TOKEN, '/', path.strip('/')])


def gen_delay(task):
    return random.uniform(2, 3) ** task.request.retries
