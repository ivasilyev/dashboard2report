
import os
import logging
import sqlalchemy
import pandas as pd
from constants import SECRET_JSON_PATH
from utils import load_dict, dump_tsv, datetime_now, join_str_lines


class SqlDBHandler:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self._secret_dict = dict()
        self.update_secret()
        self.engine = sqlalchemy.create_engine(self._secret_dict["sql_db_uri"])
        self.client = self.engine.connect().execution_options(autocommit=True)

    def __del__(self):
        self.client.close()

    def update_secret(self, file: str = SECRET_JSON_PATH):
        try:
            self._secret_dict.update(load_dict(file))
        except Exception:
            logging.critical(f"The secret file is invalid: '{file}'")
            raise

    def query_to_df(self, query: str):
        q = join_str_lines(query)
        logging.debug("Execute query: '{}'".format(q))
        df = pd.read_sql(sqlalchemy.text(query), con=self.client)
        logging.debug(f"Parsed dataframe with shape '{df.shape}' and columns '{df.columns}'")
        dump_tsv(df, os.path.join(
            self.output_dir, f"""sql-{datetime_now()}.tsv"""
        ))
        return df
