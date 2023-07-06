
import sqlalchemy
import pandas as pd
from db_handler import DBHandler


class SqlDBHandler(DBHandler):
    def __init__(self):
        super().__init__()
        self.engine = sqlalchemy.create_engine(self._secret_dict["sql_db_uri"])
        self.client = self.engine.connect().execution_options(autocommit=True)
        self.export_prefix = "sql"

    def __del__(self):
        self.client.close()
        super().__del__()

    def query_to_df(self, query: str):
        q = super().query_to_df(query)
        df = pd.read_sql(sqlalchemy.text(q), con=self.client)
        return df
