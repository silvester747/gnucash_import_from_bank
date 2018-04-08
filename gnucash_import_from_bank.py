#!/usr/bin/env python3
# coding=utf-8

import locale
import os
import sys

from gnucash_import_converter.gnucash import GnuCashCsvWriter
from gnucash_import_converter.rabobank import RabobankCsvReader

assert len(sys.argv) == 2

locale.setlocale(locale.LC_ALL, "")

with GnuCashCsvWriter(os.getcwd()) as gnucash_writer:
    with RabobankCsvReader(sys.argv[1]) as rabo_reader:
        for statement in rabo_reader:
            gnucash_writer.write_statement(statement)

