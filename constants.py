import os

LOGGING_TEMPLATE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
TIMEZONE = "Europe/Moscow"
STRAIGHT_DATETIME = "%d.%m.%Y %H:%M:%S"
REVERSED_DATETIME = "%Y-%m-%d-%H-%M-%S"
SECRET_JSON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "secret.json")
