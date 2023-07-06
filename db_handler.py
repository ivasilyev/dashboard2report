

import os
import logging
from secret import secret_dict
from utils import datetime_now, dump_tsv, join_str_lines


class DBHandler:
    def __init__(self):
        self.client = None
        self.export_prefix = ""
        self.uri = ""
        self._secret_dict = secret_dict

    def __del__(self):
        del self.client

    def query_to_df(self, query: str):
        q = join_str_lines(query)
        logging.debug(f"Execute {self.export_prefix} query: `" + q + "`")
        return q

    def export_df(self, df, output_dir):
        dump_tsv(df, os.path.join(output_dir, f"{self.export_prefix}-{datetime_now()}.tsv"))

    def process_query(self, query: str, output_dir: str):
        df = self.query_to_df(query)
        self.export_df(df, output_dir)
