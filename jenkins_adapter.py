#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
from json import dumps
from constants import LOGGING_TEMPLATE
from msword_handler import MSWordHandler


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="Jenkins adapter for Grafana2M$Word",
    )
    parser.add_argument("-l", "--link", metavar="<str>", required=True, type=str,
                        help="URI to any Grafana dashboard with the required time range selected")
    parser.add_argument("-o", "--output", metavar="<directory>", required=True,
                        help="Output directory")
    _namespace = parser.parse_args()
    return (
        _namespace.link,
        _namespace.output,
    )


def parse_link(link: str):
    try:
        d = {
            "time_from": int(re.findall("&from=([0-9]+)", link)[0]),
            "time_to": int(re.findall("&to=([0-9]+)", link)[0]),
        }
        logging.info(f"Parsed parameters: '{dumps(d)}'")
        return d
    except IndexError:
        logging.critical(f"Cannot parse the URI, exit: '{link}'")
        raise


if __name__ == '__main__':
    (
        input_link,
        input_dir
    ) = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_TEMPLATE
    )

    link_dict = parse_link(input_link)

    handler = MSWordHandler(
        time_from=link_dict["time_from"],
        time_to=link_dict["time_to"],
        title="Результаты теста"
    )
    handler.run(input_dir)
