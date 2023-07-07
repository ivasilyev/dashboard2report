#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from env import get_logging_level
from constants import LOGGING_TEMPLATE
from examples import ExampleWordExporter


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="The tool to get images from Grafana dashboard based on timestamps and place it into Word document",
        epilog="Each timestamp must be of epoch milliseconds (as Grafana provides). \n"
               "It is also highly recommended to encapsulate all the panels into spoiler row panels."
    )
    parser.add_argument("-d", "--dashboard", metavar="<uid>", required=True,
                        help="Grafana dashboard UID containing 9 letters or digits")
    parser.add_argument("-s", "--start", metavar="<timestamp>", required=True, type=int,
                        help="Timestamp of test start")
    parser.add_argument("-e", "--end", metavar="<timestamp>", required=True, type=int,
                        help="Timestamp of test end")
    parser.add_argument("-o", "--output", metavar="<directory>", default="",
                        help="Output directory")
    _namespace = parser.parse_args()
    return (
        _namespace.dashboard,
        _namespace.start,
        _namespace.end,
        _namespace.output,
    )


if __name__ == '__main__':
    (
        input_dashboard_id,
        input_time_from,
        input_time_to,
        input_dir
    ) = parse_args()

    logger = logging.getLogger()
    logger.setLevel(get_logging_level())
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter(LOGGING_TEMPLATE))
    logger.addHandler(stream)

    exporter = ExampleWordExporter(
        time_from=input_time_from,
        time_to=input_time_to,
        title="Результаты теста"
    )
    exporter.run(input_dir, render_kwargs=dict(dashboard_id=input_dashboard_id))
