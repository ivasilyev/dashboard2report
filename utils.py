
import os
import logging
import pandas as pd
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


def dump_tsv(df: pd.DataFrame, file: str):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    df.to_csv(file, sep="\t", header=True, index=False)
    logging.info(f"Saved dataframe of shape {df.shape} into file '{file}'")


def count_mma_from_df(df: pd.DataFrame):
    metrics = list()
    for column in df.columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            continue
        metrics.append(dict(
            column_name=column,
            mean=df[column].min(),
            max=df[column].max(),
            avg=df[column].mean()
        ))
    return pd.DataFrame(metrics).set_index("column_name")


def grouping_count_mma_from_df(df: pd.DataFrame, grouping_col_name: str, value_col_name: str):
    return pd.concat([
        df.groupby(grouping_col_name).min().rename(columns={value_col_name: "min"}),
        df.groupby(grouping_col_name).max().rename(columns={value_col_name: "max"}),
        df.groupby(grouping_col_name).mean().rename(columns={value_col_name: "avg"}),
    ], axis=1, sort=False)


def join_str_lines(s: str):
    from re import sub
    return sub("[\t\r\n ]+", " ", s)


def count_apdex(times: list, sla: float):
    n = len(times)
    ns = 0
    nt = 0
    for t in times:
        if t < sla:
            ns += 1
        elif sla <= t < 4 * sla:
            nt += 1
    return (ns + (nt / 2)) / n


def replace_df1_values_by_df2(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    replacing_col_name: str,
    replacement_col_name: str,
):
    replacing_dict = {
        i[0]: i[1]
        for i in df2.loc[
             :,
             [replacing_col_name, replacement_col_name]
         ].to_dict("split")["data"]
    }
    return df1.replace(replacing_dict)


def format_df_numeric_values(df: pd.DataFrame, fmt: str = "{:.1f}"):
    for column in df.columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            continue
        df[column] = df[column].apply(fmt.format)
    return df
