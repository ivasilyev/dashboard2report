
import pandas as pd
from env import TIMEZONE
from utils import parse_epoch
from msword_exporter import MSWordExporter
from confluence_exporter import ConfluenceExporter
from grafana_dashboard_handler import GrafanaDashboardHandler


class ExampleWordExporter(MSWordExporter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, output_dir: str, dashboard_id: str):
        self.add_header(self.title, 1)

        self.add_df(
            df=pd.DataFrame([
                {"Name": "Start time", "Date and time": parse_epoch(self.time_from)},
                {"Name": "End time", "Date and time": parse_epoch(self.time_to)}
            ]),
            title=f"Test date and time ({TIMEZONE})",
        )

        grafana_dashboard_handler = GrafanaDashboardHandler.from_remote(
            dashboard_id=dashboard_id,
            time_from=self.time_from,
            time_to=self.time_to,
            output_dir=output_dir
        )
        grafana_dashboard_handler.download(output_dir)
        dashboard_rows = grafana_dashboard_handler.rows

        for row_name, handlers in dashboard_rows.items():
            self.add_header(row_name, 2)
            for handler in handlers:
                self.add_image(handler=handler)

        self.add_paragraph()


class ExampleConfluenceExporter(ConfluenceExporter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, output_dir: str, dashboard_id: str):
        self.add_header(self.title, 1)

        self.add_df(
            df=pd.DataFrame([
                {"Name": "Start time", "Date and time": parse_epoch(self.time_from)},
                {"Name": "End time", "Date and time": parse_epoch(self.time_to)}
            ]),
            title=f"Test date and time ({TIMEZONE})",
        )

        grafana_dashboard_handler = GrafanaDashboardHandler.from_remote(
            dashboard_id=dashboard_id,
            time_from=self.time_from,
            time_to=self.time_to,
            output_dir=output_dir
        )
        grafana_dashboard_handler.download(output_dir)
        dashboard_rows = grafana_dashboard_handler.rows

        for row_name, handlers in dashboard_rows.items():
            self.add_header(row_name, 2)
            for handler in handlers:
                self.add_image(handler=handler)

        self.add_paragraph()
