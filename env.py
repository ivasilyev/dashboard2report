
import logging
from os import getenv as ge
from constants import (
    _LOGGING_LEVEL,
    AVAILABLE_LOGGING_LEVELS,
    _TIMEZONE,
    _CONFIG_JSON_PATH,
    _SECRET_JSON_PATH,
    _GF_PANEL_WIDTH,
    _GF_PANEL_HEIGHT,
    _TABLE_OF_CONTENTS_CAPTION
)
TIMEZONE = ge("TIMEZONE", default=_TIMEZONE)
SECRET_JSON_PATH = ge("SECRET_JSON_PATH", default=_SECRET_JSON_PATH)
CONFIG_JSON_PATH = ge("CONFIG_JSON_PATH", default=_CONFIG_JSON_PATH)

GF_PANEL_WIDTH = ge("GF_PANEL_WIDTH", default=_GF_PANEL_WIDTH)
GF_PANEL_HEIGHT = ge("GF_PANEL_HEIGHT", default=_GF_PANEL_HEIGHT)

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
