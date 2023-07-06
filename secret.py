
import logging
from os import getenv
from utils import load_dict
from constants import SECRET_JSON_PATH

_secret_file = getenv("SECRET_JSON_PATH", default=SECRET_JSON_PATH)

try:
    logging.debug(f"Using secret file: '{getenv}'")
    secret_dict = load_dict(_secret_file)
except Exception:
    logging.critical(f"The secret file is invalid: '{getenv}'")
    raise
