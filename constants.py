import os

LOGGING_TEMPLATE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
TIMEZONE = "Europe/Moscow"
INFLUXDB_INDEX_COLUMN = "time"
INFLUXDB_DATETIME = "%Y-%m-%d %H:%M:%S"
STRAIGHT_DATETIME = "%d.%m.%Y %H:%M:%S"
REVERSED_DATETIME = "%Y-%m-%d-%H-%M-%S-%f"
SECRET_JSON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "secret.json")

DEFAULT_TABLE_OF_CONTENTS_CAPTION = "Содержание"

CONFLUENCE_ATTACHMENT_SIZE_LIMIT = 30 << 20  # 30 MB

# https://confluence.atlassian.com/conf710/confluence-storage-format-1031840114.html#ConfluenceStorageFormat-Links
# <ac:link>...</ac:link>
CONFLUENCE_TEMPLATE_HYPERLINK = """
<ri:attachment ri:filename="{basename}" />
<ac:plain-text-link-body>
    <![CDATA[{link_text}]]>
</ac:plain-text-link-body>
"""

# https://confluence.atlassian.com/conf59/expand-macro-792499106.html
# https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html
# <ac:structured-macro ac:name="expand">...</ac:structured-macro>
CONFLUENCE_TEMPLATE_SPOILED_IMAGE = """
<ac:parameter ac:name="title">{filename}</ac:parameter>
<ac:rich-text-body>
    <ac:image 
        ac:alt="{filename}" 
        ac:height="100%"
        ac:thumbnail="false" 
        ac:title="{filename}"
        ac:width="100%"
    >
        <ri:attachment ri:filename="{basename}" />
    </ac:image>
</ac:rich-text-body>
"""
