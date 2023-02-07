
import os
import logging
from datetime import datetime
from constants import TIMEZONE, REVERSED_DATETIME, STRAIGHT_DATETIME


def get_file(
        url: str,
        file: str = "",
        force: bool = True,
        headers=None
):
    from requests import get
    logging.debug(f"Download URL: '{url}'")
    if os.path.isfile(file) and not force:
        logging.debug(f"Skip already downloaded file: '{file}'")
        return file
    if headers is None:
        headers = dict()
    else:
        logging.debug(f"Supplied headers: '{list(headers.keys())}'")
    response = get(url, headers=headers, stream=True)
    if response.status_code != 200:
        logging.warning(f"Got response with status {response.status_code} for '{url}'")
    if len(file) == 0:
        file = os.path.basename(url)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "wb") as f:
        for data in response.iter_content():
            f.write(data)
        f.close()
        logging.debug(f"Downloaded: '{file}'")
    return file


def load_string(file: str):
    logging.debug(f"Reading '{file}'")
    with open(file=file, mode="r", encoding="utf-8") as f:
        s = f.read()
        f.close()
    return s


def load_dict(file: str):
    from json import loads
    return loads(load_string(file))


def datetime_now(fmt: str = REVERSED_DATETIME):
    return datetime.now().strftime(fmt)


def parse_epoch(timestamp: int, fmt: str = STRAIGHT_DATETIME):
    from pytz import timezone
    tz = timezone(TIMEZONE)
    return tz.localize(datetime.fromtimestamp(timestamp / 1000)).strftime(fmt)


def dump_tsv(df, file: str):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    df.to_csv(file, sep="\t", header=True, index=False)
    logging.debug(f"Saved dataframe of shape {df.shape} into file '{file}'")
