
import logging
import atlassian
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from secret import secret_dict
from exporter import Exporter
from constants import DEFAULT_TABLE_OF_CONTENTS_CAPTION


def create_tag(tag: str, value: str = "", attrs: dict = None) -> Tag:
    tag = str(tag)
    value = str(value)
    open_tag = f"<{tag}>"
    if attrs is not None and isinstance(attrs, dict):
        open_tag = "<{} {}>".format(
            tag,
            " ".join(f"{k}=\"{v}\"" for k, v in attrs.items())
        )
    return BeautifulSoup(
        open_tag + value + f"</{tag}>", "html.parser"  # Keeps elements like '<![CDATA[...]]>'
    ).find(f"{tag}")


class ConfluenceExporter(Exporter):
    def __init__(
        self,
        time_from: int,
        time_to: int,
        secret_file: str,
        confluence_space_name: str,
        confluence_parent_page_name: str
    ):
        super().__init__(time_from=time_from, time_to=time_to)
        self.document = BeautifulSoup()
        self.client = None
        self.is_connected = False
        self.space_key = ""
        self.parent_page_id = ""
        self.confluence_space_name = confluence_space_name
        self.confluence_parent_page_name = confluence_parent_page_name

    def connect(self):
        self.client = atlassian.Confluence(
            url=secret_dict["confluence_root_url"],
            username=secret_dict["confluence_username"],
            password=secret_dict["confluence_password"]
        )
        self.space_key = [
            i for i in self.client.get_all_spaces()["results"]
            if i["name"] == self.confluence_space_name
        ][0]["key"]
        self.parent_page_id = self.client.get_page_id(
            self.space_key,
            self.confluence_parent_page_name
        )
        self.is_connected = True
        logging.debug("Confluence client connected")

    def _add(self, *args, **kwargs):
        self.document.append(create_tag(*args, **kwargs))

    def add_table_of_contents(self, caption: str = DEFAULT_TABLE_OF_CONTENTS_CAPTION):
        self._add("p", f"<b id=\"toc\">{caption}</b><ac:structured-macro ac:name=\"toc\" />")

    def add_header(self, level: int, caption: str):
        self._add(f"h{level}", str(caption))

    def add_paragraph(self, text: str):
        self._add("p", str(text))

    def add_df(self, df: pd.DataFrame):
        self._add("div", df.to_html(), {"class": "table"})

    def add_image(self, image: bytes, caption: str):
        pass

    def push_html(self, page_title: str, page_body: str):
        if not self.is_connected:
            logging.warning("Confluence client is not connected")
            return
        if self.client.page_exists(self.space_key, page_title, type=None):
            logging.debug("Update the page with the name '{}' into the space with the key '{}'".format(
                page_title, self.space_key
            ))
            o = self.client.update_page(
                page_id=self.client.get_page_id(self.space_key, page_title),
                title=page_title,
                body=page_body,
                parent_id=self.parent_page_id,
                type="page",
                representation="storage",
                minor_edit=False,
                full_width=False
            )
        else:
            logging.debug("Create the page with the name '{}' into the space with the key '{}'".format(
                page_title, self.space_key
            ))
            o = self.client.create_page(
                space=self.space_key,
                title=page_title,
                body=page_body,
                parent_id=self.parent_page_id,
                type="page",
                representation="storage",
                editor="v2",
                full_width=False
            )

    def push_blob(self, file_content: bytes, file_basename: str, page_title: str):
        logging.debug(f"Upload attachment '{file_basename}' into created page '{page_title}'")
        o = self.client.attach_content(
            content=bytes(file_content),
            name=file_basename,
            page_id=self.client.get_page_id(self.space_key, page_title),
            title=page_title,
            space=self.space_key
        )

    def push_page(self, page_title: str, page_body: str, page_attachments: list):
        logging.debug(f"Upload page {page_title} with {len(page_attachments)} attachments")
        self.push_html(page_title, page_body)
        for attachment_dict in page_attachments:
            self.push_blob(page_title=page_title, **attachment_dict)

