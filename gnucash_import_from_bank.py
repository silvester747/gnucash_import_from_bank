#!/usr/bin/env python3
# coding=utf-8

import argparse
import locale
import os

from gnucash_import_converter.gnucash import GnuCashCsvWriter
from gnucash_import_converter.rabobank import RabobankCsvReader

parser = argparse.ArgumentParser(
        description="Convert bank statements into format to import into GNUCash."
        )
parser.add_argument(
        'input_file',
        metavar='INPUT_FILE',
        action='store',
        type=str,
        help='Transaction file to import.'
        )
parser.add_argument(
        '-o', '--output_dir',
        action='store',
        default=os.getcwd(),
        type=str,
        required=False,
        help='Directory to store files to import into GNUCash. Defaults to the current working directory.'
        )
args = parser.parse_args()

locale.setlocale(locale.LC_ALL, "")

with GnuCashCsvWriter(args.output_dir) as gnucash_writer:
    with RabobankCsvReader(args.input_file) as rabo_reader:
        for statement in rabo_reader:
            gnucash_writer.write_statement(statement)

