# coding=utf-8

import csv
import io
import locale

from .gnucash import GnuCashStatement

class RabobankCsvIterator(object):
    IN_FIELDS = (
            "IBAN/BBAN",
            "Munt",
            "BIC",
            "Volgnr",
            "Datum",
            "Rentedatum",
            "Bedrag",
            "Saldo na trn",
            "Tegenrekening IBAN/BBAN",
            "Naam tegenpartij",
            "Naam uiteindelijke partij",
            "Naam initiërende partij",
            "BIC tegenpartij",
            "Code",
            "Batch ID",
            "Transactiereferentie",
            "Machtigingskenmerk",
            "Incassant ID",
            "Betalingskenmerk",
            "Omschrijving-1",
            "Omschrijving-2",
            "Omschrijving-3",
            "Reden retour",
            "Oorspr bedrag",
            "Oorspr munt",
            "Koers"
            )

    def __init__(self, csv_reader):
        self._csv_reader = csv_reader

    def __iter__(self):
        return self

    def __next__(self):
        # StopIteration will be thrown by csv reader if end of file is reached
        line = next(self._csv_reader)
        while not self._is_valid_line(line):
            line = next(self._csv_reader)

        data = dict(zip(self.IN_FIELDS, line))
        statement = GnuCashStatement()

        statement.account = data["IBAN/BBAN"]
        statement.num = data["Volgnr"]

        statement.deposit = 0
        statement.withdrawal = 0
        amount = self._read_number(data["Bedrag"])
        if amount > 0:
            statement.deposit = locale.currency(amount, "")
        else:
            statement.withdrawal = locale.currency(-amount, "")
        statement.balance = locale.currency(self._read_number(data["Saldo na trn"]), "")

        statement.date = data["Datum"]

        payee = ""
        if data["Naam uiteindelijke partij"]:
            payee = data["Naam uiteindelijke partij"]
        elif data["Naam tegenpartij"]:
            payee = data["Naam tegenpartij"]

        if not payee and data["Tegenrekening IBAN/BBAN"]:
            statement.description = data["Tegenrekening IBAN/BBAN"]
        elif data["Tegenrekening IBAN/BBAN"]:
            statement.description = "{} ({})".format(payee, data["Tegenrekening IBAN/BBAN"])
        else:
            statement.description = payee

        statement.notes = ""
        for field in ("Betalingskenmerk", "Omschrijving-1", "Omschrijving-2", "Omschrijving-3", "Reden retour"):
            if data[field]:
                statement.notes += data[field]

        return statement

    def _is_valid_line(self, line):
        return len(line) == len(self.IN_FIELDS) \
           and line[0] != "IBAN/BBAN"

    @staticmethod
    def _read_number(source):
        source = source.replace(",", ".")
        return float(source)


class RabobankCsvReader(object):
    """
    Reads new CSV format available from Rabobank Internet Bankieren.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self._csv_file = io.open(file_name, mode="r", encoding="latin-1", newline="")
        self._csv_reader = csv.reader(self._csv_file)

    def close(self):
        self._csv_reader = None
        if self._csv_file is not None:
            self._csv_file.close
            self._csv_file = None

    def __iter__(self):
        return RabobankCsvIterator(self._csv_reader)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
