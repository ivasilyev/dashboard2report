
import logging
from env import CONFIG_JSON_PATH
from utils import load_dict, is_dict_valid

try:
    logging.debug(f"Use the config file: '{CONFIG_JSON_PATH}'")
    _config_dict = load_dict(CONFIG_JSON_PATH)
except Exception:
    logging.critical(f"The config file is invalid: '{CONFIG_JSON_PATH}'")
    raise

variables = dict()
if is_dict_valid(_config_dict.get("variable")):
    variables = dict(_config_dict["variable"])

is_verify_ssl = True
if isinstance(_config_dict.get("verify_ssl"), bool):
    is_verify_ssl = bool(_config_dict["verify_ssl"])
