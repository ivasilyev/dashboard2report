
import os
import logging
import atlassian
import pandas as pd
from time import sleep
from urllib import parse
from file_handler import FileHandler
from bs4 import BeautifulSoup
from bs4.element import Tag
import config
from secret import secret_dict
from exporter import Exporter
from constants import CONFLUENCE_DELAY_SECONDS, CONFLUENCE_PUSH_ATTEMPTS, CONFLUENCE_TEMPLATE_SPOILED_IMAGE


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
    def __init__(self, parent_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = BeautifulSoup()
        self.client = None
        self.is_connected = False
        self.root_url = ""
        self.parent_page_id = ""
        self.space_key = ""
        self.attachments = dict()
        self.confluence_space_name = secret_dict["confluence_space_name"]
        self.confluence_parent_page_name = secret_dict["confluence_parent_page_name"]
        self._parse_url(parent_url)

    def _parse_url(self, url: str):
        result = parse.urlparse(parse.unquote(url))
        self.root_url = parse.urlunsplit([result.scheme, result.netloc] + ["", ] * 3)
        self.parent_page_id = parse.parse_qs(result.query)["pageId"][0]

    def connect(self):
        self.client = atlassian.Confluence(
            url=self.root_url,
            username=secret_dict["confluence_username"],
            password=secret_dict["confluence_password"],
            verify_ssl=config.confluence_is_verify_ssl
        )
        self.is_connected = True
        self.space_key = self.client.get_page_space(self.parent_page_id)
        logging.debug("Confluence client connected")

    def _add(self, *args, **kwargs):
        self.document.append(create_tag(*args, **kwargs))

    def add_table_of_contents(self):
        self._add("p", f"<b id=\"toc\">{config.confluence_table_of_contents_caption}</b><ac:structured-macro ac:name=\"toc\" />")

    def add_header(self, caption: str, level: int):
        self._add(f"h{level}", str(caption))

    def add_paragraph(self, text: str = ""):
        self._add("p", str(text))

    def add_df(self, df: pd.DataFrame, title: str = "", description: str = ""):
        if len(title) == 0 and hasattr(df, "name"):
            title = df.name
        super().add_df()
        title = f"<b>Таблица {self._table_counter}</b> – {title}"
        self.add_paragraph(title)
        self._add("div", df.to_html(header=True, index=False), {"class": "table"})
        if len(description) > 0:
            self.add_paragraph(description)

    def add_image(self, handler: FileHandler, title: str = "", description: str = ""):
        if not os.path.isfile(handler.file):
            logging.critical("The image file does not exist")
            return Tag()
        if len(title) == 0:
            title = handler.title
        logging.debug(f"Add image '{title}'")
        body = CONFLUENCE_TEMPLATE_SPOILED_IMAGE.format(
            title=title,
            basename=handler.basename,
        )
        self.attachments[title] = handler
        self._add("ac:structured-macro", body, {"ac:name": "expand"})
        super().add_image()
        self.add_paragraph(f"<b>Рисунок {self._image_counter}</b> – {title}")
        if len(description) > 0:
            self.add_paragraph(description)
        self.add_paragraph()

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

    def push_blob(self, handler: FileHandler, page_title: str):
        logging.debug(f"Upload attachment '{handler.basename}' into created page '{page_title}'")
        handler.load()
        o = self.client.attach_content(
            content=bytes(handler.content),
            name=handler.basename,
            page_id=self.client.get_page_id(self.space_key, page_title),
            title=page_title,
            space=self.space_key
        )

    def save(self):
        page_body = "".join(str(i) for i in self.document)
        for attempt in range(CONFLUENCE_PUSH_ATTEMPTS):
            try:
                logging.debug("Upload page '{}' with {} attachments for attempt {}".format(
                    self.title,
                    len(self.attachments.keys()),
                    attempt + 1,
                    CONFLUENCE_PUSH_ATTEMPTS)
                )
                self.push_html(self.title, page_body)
                break
            except:
                sleep(CONFLUENCE_DELAY_SECONDS)
        for attachment_name, handler in self.attachments.items():
            for attempt in range(CONFLUENCE_PUSH_ATTEMPTS):
                try:
                    logging.debug("Upload attachment '{}' for attempt {} of {}".format(
                        handler.title,
                        attempt + 1,
                        CONFLUENCE_PUSH_ATTEMPTS)
                    )
                    self.push_blob(handler, self.title)
                    break
                except:
                    sleep(CONFLUENCE_DELAY_SECONDS)

    def run(self, output_dir: str, render_kwargs: dict):
        self.connect()
        logging.debug("Started document creation")
        self.render(output_dir, **render_kwargs)
        logging.debug("Finished document creation")
        self.save()
        logging.debug("Finished document upload")
