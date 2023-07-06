
import pandas as pd
from db_handler import DBHandler
from urllib.parse import urlparse
from influxdb import InfluxDBClient as Client


class InfluxDBHandler(DBHandler):
    def __init__(self):
        super().__init__()
        self.uri = self._secret_dict["influx_server_url"]
        parsed = urlparse(self.uri)
        self.client = Client(
            host=parsed.hostname,
            port=parsed.port,
            database=self._secret_dict["influx_db_name"]
        )
        self.export_prefix = "influx"

    def __del__(self):
        self.client.close()
        super().__del__()

    def query_to_df(self, query: str):
        q = super().query_to_df(query)
        df = pd.DataFrame(self.client.query(q).get_points())
        return df
