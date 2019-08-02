# coding=utf-8
"""
Main application for converting bank statements.
"""

import argparse
import locale
import os
import sys

from gnucash_import_converter.gnucash import GnuCashCsvWriter
from gnucash_import_converter.rabobank import RabobankCsvReader
from gnucash_import_converter.abnamro import AbnAmroTxtReader

def main(argv=None):
    """
    Main application for converting bank statements.
    """
    supported_readers = {
        'rabobank': RabobankCsvReader,
        'abnamro': AbnAmroTxtReader,
    }

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
        '-t', '--type',
        action='store',
        type=str,
        choices=supported_readers,
        required=True,
        help='Type of transaction file to import.',
    )
    parser.add_argument(
        '-o', '--output_dir',
        action='store',
        default=os.getcwd(),
        type=str,
        required=False,
        help='Directory to store files to import into GNUCash. Defaults to the current working ' + \
             'directory.'
    )
    parser.add_argument(
        '-m', '--split-months',
        action='store_true',
        help='Create separate files for each month.'
    )

    args = parser.parse_args(argv)

    locale.setlocale(locale.LC_ALL, "")

    with GnuCashCsvWriter(args.output_dir, args.split_months) as gnucash_writer:
        with supported_readers[args.type](args.input_file) as rabo_reader:
            for statement in rabo_reader:
                gnucash_writer.write_statement(statement)
