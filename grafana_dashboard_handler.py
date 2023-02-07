
import os
import logging
from grafana_panel_handler import GrafanaPanelHandler


class GrafanaDashboardHandler:
    def __init__(
        self,
        dashboard_id: str,
        dashboard_alias: str,
        time_from: int,
        time_to: int,
        panels: dict,
        query_params=None,
    ):
        self.dashboard_id = dashboard_id
        self.dashboard_alias = dashboard_alias
        self.time_from = time_from
        self.time_to = time_to
        self.panels = panels
        self.panel_handlers = dict()

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

    def download(self, output_dir: str = os.getcwd()):
        for i in self.panel_handlers.values():
            logging.debug(f"Download dashboard with alias '{self.dashboard_alias}' into '{output_dir}'")
            i.download(output_dir)
