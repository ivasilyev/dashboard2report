
import os
import logging
import pandas as pd
from influxdb import InfluxDBClient as Client
from utils import load_dict, dump_tsv, datetime_now
from constants import SECRET_JSON_PATH

from urllib.parse import urlparse


class InfluxDBHandler:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self._secret_dict = dict()
        self.update_secret()
        uri = urlparse(self._secret_dict["influx_server_url"])
        self.client = Client(
            host=uri.hostname,
            port=uri.port,
            database=self._secret_dict["influx_db_name"]
        )

    def __del__(self):
        self.client.close()

    def update_secret(self, file: str = SECRET_JSON_PATH):
        try:
            self._secret_dict.update(load_dict(file))
        except Exception:
            logging.critical(f"The secret file is invalid : '{file}'")
            raise

    def query_to_df(self, query: str):
        logging.debug("Execute query: {}".format(query))
        df = pd.DataFrame(self.client.query(query).get_points())
        logging.debug(f"Parsed dataframe with shape '{df.shape}' and columns '{df.columns}'")
        dump_tsv(df, os.path.join(
            self.output_dir, f"""influx-{self._secret_dict["influx_db_name"]}-{datetime_now()}.tsv"""
        ))
        return df

