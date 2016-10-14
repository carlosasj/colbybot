import re

TITLE_LABEL = r'^[^:{}]+$'
TITLE_KEY = r'^{([^:{}]+)}$'
TITLE_KEY_DEFAULT = r'^{([^:{}]+):([^:{}]+)}$'


def parse_title(params):
    if "title" not in params:
        return {
            "key": None,
            "default": None,
        }
    if isinstance(params["title"], list):
        title = params["title"][0]
    else:
        title = params["title"]

    match_label = re.compile(TITLE_LABEL).match(title)
    match_key = re.compile(TITLE_KEY).match(title)
    match_key_default = re.compile(TITLE_KEY_DEFAULT).match(title)

    if not any((bool(match_label),
                bool(match_key),
                bool(match_key_default))):
        return {
            "key": None,
            "default": None,
        }

    if match_key_default:
        groups = match_key_default.groups()
        return {
            "key": groups[0],
            "default": groups[1],
        }
    elif match_key:
        groups = match_key.groups()
        return {
            "key": groups[0],
            "default": None,
        }
    else:
        return {
            "key": None,
            "default": title,
        }


KEYS_KEY = r'^[^:{}]+$'
KEYS_KEY_LABEL = r'^([^:{}]+):([^:{}]+)$'
KEYS_KEY_LABEL_DEFAULT = r'^([^:{}]+):([^:{}]+):([^:{}]*)$'
KEYS_EMPTY = r'^::$'


def parse_key(item):
    if re.compile(KEYS_EMPTY).match(item):
        return {
            "key": None,
            "label": "\n",
            "default": "\n",
        }

    match_key_label_default = re.compile(KEYS_KEY_LABEL_DEFAULT).match(item)
    match_key_label = re.compile(KEYS_KEY_LABEL).match(item)
    match_key = re.compile(KEYS_KEY).match(item)
    if not any((bool(match_key_label_default),
                bool(match_key_label),
                bool(match_key))):
        return None

    if match_key_label_default:
        groups = match_key_label_default.groups()
        return {
            "key": groups[0],
            "label": groups[1],
            "default": groups[2],
        }
    elif match_key_label:
        groups = match_key_label.groups()
        return {
            "key": groups[0],
            "label": groups[1],
            "default": None,
        }
    else:
        return {
            "key": item,
            "label": item,
            "default": None,
        }


def parse_keys(params):
    if "keys" not in params:
        return []

    keys = params["keys"]
    if isinstance(keys, list):
        keys = ','.join(params["keys"])

    keys = keys.split(',')
    parsed = [parse_key(k) for k in keys]
    parsed = [p for p in parsed if p is not None]
    return parsed


def parse(params):
    return {
        "title": parse_title(params),
        "keys": parse_keys(params),
    }
