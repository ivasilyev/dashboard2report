
import logging
from utils import load_dict
from env import SECRET_JSON_PATH

try:
    logging.debug(f"Using secret file: '{SECRET_JSON_PATH}'")
    secret_dict = load_dict(SECRET_JSON_PATH)
except Exception:
    logging.critical(f"The secret file is invalid: '{SECRET_JSON_PATH}'")
    raise
