
import os
import logging
import urllib.parse as urlparse
from urllib.parse import urlencode
from secret import secret_dict
from constants import TIMEZONE
from image_handler import ImageHandler
from utils import is_dict_valid, get_file, datetime_now


class GrafanaPanelHandler(ImageHandler):
    def __init__(
        self,
        title: str,
        time_from: int,
        time_to: int,
        file: str = "",
        dashboard_id: str = "",
        dashboard_alias: str = "",
        server_name: str = "",
        panel_id: str = "",
        query_params: dict = None,
        description: str = "",
        row_name: str = "",
    ):
        super().__init__(title, file, description)
        self.dashboard_id = dashboard_id
        self.dashboard_alias = dashboard_alias
        self.row_name = row_name
        self.time_from = time_from
        self.time_to = time_to
        self.server_name = server_name
        self.panel_id = panel_id
        self.query_params = query_params
        if is_dict_valid(self.query_params):
            self.query_params = dict()
        logging.debug(f"Created {self}")

    def __str__(self):
        return (
            f"Panel Handler with ID {self.panel_id} and title {self.dashboard_alias} for the time range "
            f"from {self.time_from} to {self.time_to}"
        )

    def compose_url(self):
        prefix = f"""{secret_dict["gf_server_url"]}/render/d-solo/{self.dashboard_id}/{self.dashboard_alias}"""
        parameter_dict = {
            "orgId": 1,
            "from": self.time_from,
            "to": self.time_to,
            "var-Interval": "10s",
            "theme": "light",
            "panelId": self.panel_id,
            "width": 1000,
            "height": 500,
            "tz": TIMEZONE,
        }

        url_parts = list(urlparse.urlparse(prefix))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(parameter_dict)
        query.update(self.query_params)
        url_parts[4] = urlencode(query)
        return urlparse.urlunparse(url_parts)

    def download(self, output_dir: str = os.getcwd()):
        if len(self.file) == 0:
            self.file = os.path.join(output_dir, f"panel-{self.dashboard_alias}-{self.panel_id}-{datetime_now()}.png")
        url = self.compose_url()
        get_file(
            url=url,
            file=self.file,
            headers={"Authorization": "Bearer {}".format(secret_dict["gf_token"])}
        )
        logging.info(f"Downloaded Grafana panel '{self.title}' into '{self.file}'")
