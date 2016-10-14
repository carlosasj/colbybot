from . import attribute
from ..utils import dict_to_markdown


def get_key(keys_dotted, payload, default=None):
    dikt = payload
    if keys_dotted is None:
        return default
    for key in attribute.parse(keys_dotted):
        try:
            dikt = dikt[key]
        except (KeyError, TypeError):
            try:
                dikt = dikt[int(key)]
            except (ValueError, IndexError, TypeError, KeyError):
                return default

    return dikt


def parse(params, payload):
    title = get_key(params["title"]["key"],
                    payload,
                    params["title"]["default"])
    keys = {
        key["label"].replace('\\.', '.'): get_key(key["key"],
                                                  payload,
                                                  key["default"])
        for key in params["keys"]
        if key is not None
    }
    order = [key["label"].replace('\\.', '.')
             for key in params["keys"] if key is not None]

    text = ""

    if title:
        text = "".join(["*", str(title), "*\n\n"])

    return "".join([text, dict_to_markdown(keys, order)])
