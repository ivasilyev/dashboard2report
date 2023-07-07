
import logging
from os import getenv as ge
from constants import (
    _LOGGING_LEVEL,
    AVAILABLE_LOGGING_LEVELS,
    _CONFIG_JSON_PATH,
    _SECRET_JSON_PATH,
    _TIMEZONE,
    _TABLE_OF_CONTENTS_CAPTION
)
TIMEZONE = ge("TIMEZONE", default=_TIMEZONE)
SECRET_JSON_PATH = ge("SECRET_JSON_PATH", default=_SECRET_JSON_PATH)
CONFIG_JSON_PATH = ge("CONFIG_JSON_PATH", default=_CONFIG_JSON_PATH)
TABLE_OF_CONTENTS_CAPTION = ge("TABLE_OF_CONTENTS_CAPTION", default=_TABLE_OF_CONTENTS_CAPTION)


def get_logging_level():
    out = _LOGGING_LEVEL
    try:
        level = int(ge("LOGGING_LEVEL", f"{_LOGGING_LEVEL}"))
        assert level in AVAILABLE_LOGGING_LEVELS
        out = level * 10
    except:
        logging.debug("Reset to default logging level")
    logging.debug(f"Use logging level: {out}")
    return out
