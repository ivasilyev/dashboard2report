#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from constants import LOGGING_TEMPLATE
from msword_handler import MSWordHandler


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="The tool to get images from Grafana based on timestamps and place it into Word document",
        epilog="Each timestamp must be of epoch milliseconds"
    )
    parser.add_argument("-s", "--start", metavar="<timestamp>", required=True, type=int,
                        help="Timestamp of test start")
    parser.add_argument("-e", "--end", metavar="<timestamp>", required=True, type=int,
                        help="Timestamp of test end")
    parser.add_argument("-o", "--output", metavar="<directory>", default="",
                        help="Output directory")
    _namespace = parser.parse_args()
    return (
        _namespace.start,
        _namespace.end,
        _namespace.output,
    )


if __name__ == '__main__':
    (
        input_time_from,
        input_time_to,
        input_dir
    ) = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_TEMPLATE
    )

    handler = MSWordHandler(
        time_from=input_time_from,
        time_to=input_time_to,
        title="Результаты теста"
    )
    handler.run(input_dir)
