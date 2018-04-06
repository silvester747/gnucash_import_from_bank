#!/usr/bin/python
# coding=utf-8

import csv
import locale
import os
import sys

from gnucash_import_converter.gnucash import GnuCashStatement, GnuCashCsvWriter

assert len(sys.argv) == 2
rabo_mut_file = open(sys.argv[1], "rb")

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

def read_number(source):
    source = source.replace(",", ".")
    return float(source)

locale.setlocale(locale.LC_ALL, "")

gnucash_writer = GnuCashCsvWriter(os.getcwd())

try:
    rabo_reader = csv.reader(rabo_mut_file)
    
    for line in rabo_reader:

        if len(line) < len(IN_FIELDS):
            print("Line is too short, skipping: %s" % line)
            continue
        if line[0] == "IBAN/BBAN":
            # Header row
            continue
        
        data = dict(zip(IN_FIELDS, line))
        statement = GnuCashStatement()
        
        statement.account = data["IBAN/BBAN"]
        
        statement.deposit = 0
        statement.withdrawal = 0
        amount = read_number(data["Bedrag"])
        if amount > 0:
            statement.deposit = locale.currency(amount, "")
        else:
            statement.withdrawal = locale.currency(-amount, "")
        statement.balance = locale.currency(read_number(data["Saldo na trn"]), "")
        
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

        gnucash_writer.write_statement(statement)

finally:
    gnucash_writer.close()
    rabo_mut_file.close()
