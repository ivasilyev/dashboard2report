import os

LOGGING_TEMPLATE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
TIMEZONE = "Europe/Moscow"
INFLUXDB_INDEX_COLUMN = "time"
INFLUXDB_DATETIME = "%Y-%m-%d %H:%M:%S"
STRAIGHT_DATETIME = "%d.%m.%Y %H:%M:%S"
REVERSED_DATETIME = "%Y-%m-%d-%H-%M-%S-%f"
SECRET_JSON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "secret.json")
