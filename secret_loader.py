
import logging
from utils import load_dict
from constants import SECRET_JSON_PATH


class SecretLoader:
    def __init__(self, secret_file: str = SECRET_JSON_PATH):
        self._secret_dict = dict()
        self.update_secret(secret_file)

    def update_secret(self, file):
        try:
            self._secret_dict.update(load_dict(file))
        except Exception:
            logging.critical(f"The secret file is invalid: '{file}'")
            raise
