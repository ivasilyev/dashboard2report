
import logging
import constants
from env import CONFIG_JSON_PATH
from utils import load_dict, is_dict_valid, is_bool_valid, is_int_valid, is_str_valid

try:
    logging.debug(f"Use the config file: '{CONFIG_JSON_PATH}'")
    _config_dict = load_dict(CONFIG_JSON_PATH)
except Exception:
    logging.critical(f"The config file is invalid: '{CONFIG_JSON_PATH}'")
    raise


def _get(s: str):
    return _config_dict.get(s)


variables = dict()
if is_dict_valid(_get("variables")):
    variables = dict(_get("variables"))

# See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
grafana_timezone = constants.TIMEZONE
if is_str_valid(_get("grafana_timezone")):
    grafana_timezone = str(_get("grafana_timezone"))

grafana_panel_width = 1000
if is_int_valid(_get("grafana_panel_width")):
    grafana_panel_width = int(_get("grafana_panel_width"))

grafana_panel_height = 500
if is_int_valid(_get("grafana_panel_height")):
    grafana_panel_height = int(_get("grafana_panel_height"))

msword_template_caption_table = "Table {counter} – {title}"
if is_str_valid(_get("msword_template_caption_table")):
    msword_template_caption_table = str(_get("msword_template_caption_table"))

msword_template_caption_image = "Image {counter} – {title}"
if is_str_valid(_get("msword_template_caption_image")):
    msword_template_caption_image = str(_get("msword_template_caption_image"))

confluence_template_caption_table = "<b>Table {counter}</b> – {title}"
if is_str_valid(_get("confluence_template_caption_table")):
    confluence_template_caption_table = str(_get("confluence_template_caption_table"))

confluence_template_caption_image = "<b>Image {counter}</b> – {title}"
if is_str_valid(_get("confluence_template_caption_image")):
    confluence_template_caption_image = str(_get("confluence_template_caption_image"))

confluence_is_verify_ssl = True
if is_bool_valid(_get("confluence_is_verify_ssl")):
    confluence_is_verify_ssl = bool(_get("confluence_is_verify_ssl"))

confluence_table_of_contents_caption = "Table of Contents"
if is_str_valid(_get("confluence_table_of_contents_caption")):
    confluence_table_of_contents_caption = str(_get("confluence_table_of_contents_caption"))
