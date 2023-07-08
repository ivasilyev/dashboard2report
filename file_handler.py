
import os
from utils import load_bytes, filename_only


class FileHandler:
    def __init__(
        self,
        title: str,
        file: str = "",
        description: str = "",
    ):
        self.title = title
        self.file = file
        self.description = description
        self.content = bytes()

    @property
    def basename(self):
        return os.path.basename(self.file)

    @property
    def filename(self):
        return filename_only(self.file)

    def load(self):
        self.content = load_bytes(self.file)

    def download(self, *args, **kwargs):
        pass
