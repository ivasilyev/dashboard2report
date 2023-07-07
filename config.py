
import logging
from utils import load_dict
from env import CONFIG_JSON_PATH

try:
    logging.debug(f"Use the config file: '{CONFIG_JSON_PATH}'")
    secret_dict = load_dict(CONFIG_JSON_PATH)
except Exception:
    logging.critical(f"The config file is invalid: '{CONFIG_JSON_PATH}'")
    raise
