# coding=utf-8
"""
Reading ABN Amro statements into intermediate format.
"""

import csv
import io
import re

from .gnucash import GnuCashStatement


class _AbnAmroTxtIterator(object):
    FIXED_FIELDS = (
        "Account",
        "Currency",
        "Date",
        "Balance before",
        "Balance after",
        "Interest date",
        "Amount",
        "Extra fields",
    )

    def __init__(self, csv_reader):
        self._csv_reader = csv_reader

    def __iter__(self):
        return self

    def __next__(self):
        # StopIteration will be thrown by csv reader if end of file is reached
        line = next(self._csv_reader)

        fixed_data = dict(zip(self.FIXED_FIELDS, line))
        extra_data = self._split_extra_fields(fixed_data['Extra fields'])

        statement = GnuCashStatement()
        statement.account = fixed_data['Account']

        flat_date = fixed_data['Date']
        assert len(flat_date) == 8
        statement.date = '{}-{}-{}'.format(
            flat_date[0:4], flat_date[4:6], flat_date[6:8])

        statement.balance = self._read_currency(fixed_data['Balance after'])
        statement.deposit = 0
        statement.withdrawal = 0
        amount = self._read_currency(fixed_data["Amount"])
        if amount > 0:
            statement.deposit = amount
        else:
            statement.withdrawal = -amount

        if 'Naam' in extra_data:
            if 'IBAN' in extra_data:
                statement.description = '{} ({})'.format(extra_data['Naam'],
                                                         extra_data['IBAN'])
            else:
                statement.description = extra_data['Naam']
        elif 'Rest' in extra_data:
            statement.description = self._clean_description(extra_data['Rest'])

        if 'Omschrijving' in extra_data:
            statement.notes = extra_data['Omschrijving']

        return statement

    @staticmethod
    def _split_extra_fields(extra_field_str):
        if extra_field_str.startswith('/TRTP/'):
            return _AbnAmroTxtIterator._split_extra_fields_trtp(extra_field_str)
        else:
            parts = re.split(r'\s\s+', extra_field_str)
            assert parts
            print(parts)

            extra_data = {}
            extra_data['Type'] = transaction_type = parts[0]

            if transaction_type == 'BEA':
                _AbnAmroTxtIterator._split_extra_fields_bea(parts, extra_data)
            else:
                _AbnAmroTxtIterator._split_extra_fields_generic(parts, extra_data)

            return extra_data

    @staticmethod
    def _split_extra_fields_generic(parts, extra_data):
        for item in parts[1:]:
            if ':' in item:
                key, value = re.split(r':\s?', item, maxsplit=1)

                if key in extra_data:
                    # Key might be detected as part of value
                    extra_data[key] += '  {}: {}'.format(key, value)
                else:
                    extra_data[key] = value
            else:
                if 'Rest' in extra_data:
                    extra_data['Rest'] += "," + item
                else:
                    extra_data['Rest'] = item

    @staticmethod
    def _split_extra_fields_bea(parts, extra_data):
        combined = ' '.join(parts[1:])
        match = re.search(r"\d\d\.\d\d\.\d\d/\d\d\.\d\d (.*),PAS\d+", combined)
        if match:
            extra_data['Naam'] = match.group(1)
        else:
            extra_data['Rest'] = combined

    @staticmethod
    def _split_extra_fields_trtp(extra_field_str):
        extra_data = {}

        parts = extra_field_str.split('/')
        assert len(parts) > 2
        assert parts[1] == 'TRTP'
        parts = parts[1:]
        while len(parts) >= 2:
            extra_data[parts[0]] = parts[1]
            parts = parts[2:]
        if len(parts) == 1:
            extra_data['Rest'] = parts[0]

        if 'NAME' in extra_data:
            extra_data['Naam'] = extra_data['NAME']
        if 'REMI' in extra_data:
            extra_data['Omschrijving'] = extra_data['REMI']
        return extra_data

    @staticmethod
    def _clean_description(value):
        match = re.match(r"\d\d\.\d\d\.\d\d/\d\d\.\d\d (.*),PAS\d+", value)
        if match:
            return match.group(1)
        return value

    @staticmethod
    def _read_currency(source):
        source = source.replace(",", ".")
        return float(source)


class AbnAmroTxtReader(object):
    """
    Reads TXT format available from ABN AMRO Internet Bankieren.
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self._csv_file = io.open(
            file_name, mode="r", encoding="utf-8", newline="")
        self._csv_reader = csv.reader(self._csv_file, dialect='excel-tab')

    def close(self):
        """
        Close the input file.
        """
        self._csv_reader = None
        if self._csv_file is not None:
            self._csv_file.close()
            self._csv_file = None

    def __iter__(self):
        return _AbnAmroTxtIterator(self._csv_reader)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
