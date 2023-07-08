
class Exporter:
    def __init__(
            self,
            time_from: int,
            time_to: int,
            title: str = "Document Title",
    ):
        self.time_from = time_from
        self.time_to = time_to
        self.title = title

        self.document = None
        self._image_counter = 1
        self._table_counter = 1

    def add_header(self, *args, **kwargs):
        pass

    def add_paragraph(self, *args, **kwargs):
        pass

    def add_df(self, *args, **kwargs):
        pass

    def add_blob(self, *args, **kwargs):
        pass

    def add_image(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass
