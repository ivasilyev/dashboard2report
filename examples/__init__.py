
import pandas as pd
import config
from utils import parse_epoch
from msword_exporter import MSWordExporter
from confluence_exporter import ConfluenceExporter
from grafana_dashboard_handler import GrafanaDashboardHandler


class ExampleWordExporter(MSWordExporter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, output_dir: str, dashboard_id: str):
        # Confluence pages already have a header

        self.add_paragraph("Дата и время проведения теста: {} - {}".format(
            *[parse_epoch(time_stamp=i, time_zone=config.grafana_timezone) for i in (self.time_from, self.time_to)])
        )

        grafana_dashboard_handler = GrafanaDashboardHandler.from_remote(
            dashboard_id=dashboard_id,
            time_from=self.time_from,
            time_to=self.time_to,
            output_dir=output_dir
        )
        grafana_dashboard_handler.download(output_dir)
        dashboard_rows = grafana_dashboard_handler.rows

        self.add_header("Grafana", 1)
        self.add_header(grafana_dashboard_handler.dashboard_alias, 2)
        for row_name, handlers in dashboard_rows.items():
            self.add_header(row_name, 3)
            for handler in handlers:
                self.add_image(handler=handler)

        self.add_paragraph()


class ExampleConfluenceExporter(ConfluenceExporter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, output_dir: str, dashboard_id: str):
        self.add_header(self.title, 1)
        self.add_paragraph("<b>Дата и время проведения теста:</b> {} - {}".format(
            *[parse_epoch(time_stamp=i, time_zone=config.grafana_timezone) for i in (self.time_from, self.time_to)])
        )
        grafana_dashboard_handler = GrafanaDashboardHandler.from_remote(
            dashboard_id=dashboard_id,
            time_from=self.time_from,
            time_to=self.time_to,
            output_dir=output_dir
        )
        grafana_dashboard_handler.download(output_dir)
        dashboard_rows = grafana_dashboard_handler.rows

        self.add_header("Grafana", 2)
        self.add_header(grafana_dashboard_handler.dashboard_alias, 3)
        for row_name, handlers in dashboard_rows.items():
            self.add_header(row_name, 4)
            for handler in handlers:
                self.add_image(handler=handler)

        self.add_paragraph()
