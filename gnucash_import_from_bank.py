#!/usr/bin/env python3
# coding=utf-8

import locale
import os
import sys

from gnucash_import_converter.gnucash import GnuCashCsvWriter
from gnucash_import_converter.rabobank import RabobankCsvReader

assert len(sys.argv) == 2

locale.setlocale(locale.LC_ALL, "")

gnucash_writer = GnuCashCsvWriter(os.getcwd())
rabo_reader = RabobankCsvReader(sys.argv[1])

try:
    for statement in rabo_reader:
        gnucash_writer.write_statement(statement)

finally:
    gnucash_writer.close()
    rabo_reader.close()
