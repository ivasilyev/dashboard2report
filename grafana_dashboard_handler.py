
import os
import logging
import posixpath
from collections import defaultdict
from secret import secret_dict
from utils import get_file, is_dict_valid, load_dict
from grafana_panel_handler import GrafanaPanelHandler


class GrafanaDashboardHandler:
    def __init__(
        self,
        dashboard_id: str,
        dashboard_alias: str,
        time_from: int,
        time_to: int,
        panels: dict = None,
        query_params: dict = None
    ):
        self.dashboard_id = dashboard_id
        self.dashboard_alias = dashboard_alias
        self.time_from = time_from
        self.time_to = time_to
        self.panels = panels
        self.panel_handlers = dict()

        if is_dict_valid(self.panels):
            for panel_name, panel_id in self.panels.items():
                self.panel_handlers[panel_name] = GrafanaPanelHandler(
                    title=panel_name,
                    panel_id=panel_id,
                    dashboard_id=self.dashboard_id,
                    dashboard_alias=self.dashboard_alias,
                    time_from=self.time_from,
                    time_to=self.time_to,
                    query_params=query_params,
                )
        logging.debug(f"Created {self}")

    def __str__(self):
        return (
            f"Dashboard Handler with UID {self.dashboard_id} and title {self.dashboard_alias} for the time range "
            f"from {self.time_from} to {self.time_to} with {len(self.panel_handlers.keys())} panels"
        )

    @property
    def rows(self):
        d = defaultdict(list)
        for handler in self.panel_handlers.values():
            k = handler.row_name
            if len(k) > 0:
                d[k].append(handler)
        return d

    @staticmethod
    # Import anything
    def from_dict(
        d: dict,
        time_from: int,
        time_to: int,
        query_params: dict = None
    ):
        dashboard_id = d["dashboard"]["uid"]
        dashboard_alias = d["dashboard"]["title"]
        handler = GrafanaDashboardHandler(
            dashboard_id=dashboard_id,
            dashboard_alias=dashboard_alias,
            time_from=time_from,
            time_to=time_to,
            query_params=query_params,
        )

        for panel_row_spoiler in d["dashboard"]["panels"]:
            panel_row_spoiler_title = panel_row_spoiler["title"]
            if panel_row_spoiler["type"] != "row":  # To be optimized, yet every panel *must* be in a row
                continue
            for panel in panel_row_spoiler["panels"]:
                panel_name = panel["title"]
                handler.panel_handlers[panel_name] = GrafanaPanelHandler(
                    title=panel_name,
                    panel_id=panel["id"],
                    dashboard_id=dashboard_id,
                    dashboard_alias=dashboard_alias,
                    time_from=time_from,
                    time_to=time_to,
                    query_params=query_params,
                    row_name=panel_row_spoiler_title
                )
        logging.debug(f"Loaded dashboard JSON with UID '{dashboard_id}'")
        return handler

    @staticmethod
    def from_json(file: str, **kwargs):
        logging.debug(f"Loaded dashboard JSON from file '{file}'")
        kwargs["d"] = load_dict(file)
        return GrafanaDashboardHandler.from_dict(**kwargs)

    @staticmethod
    def download_json(
        dashboard_id: str,
        output_file: str
    ):
        logging.debug(f"Download dashboard JSON with UID '{dashboard_id}' into: '{output_file}'")
        url = posixpath.join(secret_dict["gf_server_url"], "api/dashboards/uid", dashboard_id)
        get_file(
            url=url,
            file=output_file,
            headers={"Authorization": "Bearer {}".format(secret_dict["gf_token"])}
        )

    @staticmethod
    def from_remote(
        dashboard_id: str,
        output_dir: str = os.getcwd(),
        **kwargs
    ):
        output_file = os.path.join(output_dir, f"{dashboard_id}.json")
        GrafanaDashboardHandler.download_json(dashboard_id, output_file)
        return GrafanaDashboardHandler.from_json(output_file, **kwargs)

    def download(self, output_dir: str = os.getcwd()):
        for i in self.panel_handlers.values():
            logging.debug(f"Download dashboard with alias '{self.dashboard_alias}' into '{output_dir}'")
            i.download(output_dir)
