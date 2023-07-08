#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from env import get_logging_level
from utils import validate_directory
from constants import LOGGING_TEMPLATE
from examples import ExampleWordExporter, ExampleConfluenceExporter


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
    parser.add_argument("-p", "--page_name", metavar="<str>", default="",
                        help="Confluence target page name")
    _namespace = parser.parse_args()
    output_dir = validate_directory(_namespace.output)
    return (
        _namespace.dashboard,
        _namespace.start,
        _namespace.end,
        output_dir,
        _namespace.page_name,
    )


if __name__ == '__main__':
    (
        input_dashboard_id,
        input_time_from,
        input_time_to,
        input_dir,
        confluence_page_name,
    ) = parse_args()

    logger = logging.getLogger()
    logger.setLevel(get_logging_level())
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter(LOGGING_TEMPLATE))
    logger.addHandler(stream)

    word_exporter = ExampleWordExporter(
        time_from=input_time_from,
        time_to=input_time_to,
        title="Результаты теста"
    )
    word_exporter.run(input_dir, render_kwargs=dict(dashboard_id=input_dashboard_id))

    confluence_exporter = ExampleConfluenceExporter(
        time_from=input_time_from,
        time_to=input_time_to,
        title="Результаты теста"
    )
    confluence_exporter.run(
        output_dir=input_dir,
        page_title=confluence_page_name,
        render_kwargs=dict(dashboard_id=input_dashboard_id)
    )
