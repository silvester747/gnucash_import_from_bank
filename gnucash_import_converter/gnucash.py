#!/usr/bin/python
# coding=utf-8

import csv
import locale
import os


class GnuCashStatement(object):
    def __init__(self, date=None, num=None, description=None, notes=None, account=None,
            deposit=None, withdrawal=None, balance=None):
        self.date = date
        self.num = num
        self.description = description
        self.notes = notes
        self.account = account
        self.deposit = deposit
        self.withdrawal = withdrawal
        self.balance = balance


class GnuCashCsvWriter(object):
    OUT_FIELDS = (
            "Date",
    #        "Num",
            "Description",
            "Notes",
            "Account",
            "Deposit",
            "Withdrawal",
            "Balance"
            )

    def __init__(self, output_dir, split_months=False):
        self.output_dir = output_dir
        self.split_months = split_months
        os.makedirs(output_dir, exist_ok=True)

        self._open_files= []
        self._csv_writers = {}

    def write_statement(self, statement):
        self._get_writer(self._file_base_name(statement)).writerow((
                statement.date,
                statement.description,
                statement.notes,
                statement.account,
                self._currency(statement.deposit),
                self._currency(statement.withdrawal),
                self._currency(statement.balance),
                ))

    def close(self):
        for f in self._open_files:
            f.close()
        self._open_files = []

    def _get_writer(self, file_base_name):
        csv_writer = self._csv_writers.get(file_base_name, None)
        if csv_writer is not None:
            return csv_writer

        f = open(os.path.join(self.output_dir, file_base_name + ".csv"), mode="w")
        self._open_files.append(f)

        csv_writer = csv.writer(f)
        self._csv_writers[file_base_name] = csv_writer

        csv_writer.writerow(self.OUT_FIELDS)

        return csv_writer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    @staticmethod
    def _currency(value):
        return locale.currency(value, symbol=False)

    def _file_base_name(self, statement):
        if self.split_months:
            return f"{statement.account}-{statement.date[:7]}"
        else:
            return statement.account
