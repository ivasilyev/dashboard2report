
import pandas as pd
from utils import parse_epoch
from grafana_dashboard_handler import GrafanaDashboardHandler
from msword_exporter import MSWordExporter


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
            title="Test date and time",
        )

        grafana_dashboard_handler = GrafanaDashboardHandler.from_remote(
            dashboard_id=dashboard_id,
            time_from=self.time_from,
            time_to=self.time_to,
        )
        grafana_dashboard_handler.download(output_dir)
        dashboard_rows = grafana_dashboard_handler.rows

        for row_name, handlers in dashboard_rows.items():
            self.add_header(row_name, 2)
            for handler in handlers:
                self.add_image(handler=handler)

        self.add_paragraph()
