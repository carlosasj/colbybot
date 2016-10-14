import re


def parse(key):
    splitted = re.split(r'(?<!\\)\.', key)
    return [s.replace('\\.', '.') for s in splitted]
