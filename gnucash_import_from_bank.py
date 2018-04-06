#!/usr/bin/python
# coding=utf-8

import csv
import locale
import sys

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

account_files = []
account_file_writers = {}

def open_account_file_writer(account):
    account_file_writer = account_file_writers.get(account, None)
    if not account_file_writer is None:
        return account_file_writer
    
    account_file = open(account + ".csv", "wb")
    account_files.append(account_file)
    account_file_writer = csv.writer(account_file)
    account_file_writers[account] = account_file_writer
    
    account_file_writer.writerow(OUT_FIELDS)
    
    return account_file_writer
    

def read_number(source):
    source = source.replace(",", ".")
    return float(source)

locale.setlocale(locale.LC_ALL, "")

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
        
        account = data["IBAN/BBAN"]
        writer = open_account_file_writer(account)
        
        deposit = 0
        withdrawal = 0
        amount = read_number(data["Bedrag"])
        if amount > 0:
            deposit = locale.currency(amount, "")
        else:
            withdrawal = locale.currency(-amount, "")
        balance = locale.currency(read_number(data["Saldo na trn"]), "")
        
        date = data["Datum"]

        payee = ""
        if data["Naam uiteindelijke partij"]:
            payee = data["Naam uiteindelijke partij"]
        elif data["Naam tegenpartij"]:
            payee = data["Naam tegenpartij"]

        if not payee and data["Tegenrekening IBAN/BBAN"]:
            description = data["Tegenrekening IBAN/BBAN"]
        elif data["Tegenrekening IBAN/BBAN"]:
            description = "{} ({})".format(payee, data["Tegenrekening IBAN/BBAN"])
        else:
            description = payee
        
        notes = ""
        for field in ("Betalingskenmerk", "Omschrijving-1", "Omschrijving-2", "Omschrijving-3", "Reden retour"):
            if data[field]:
                notes += data[field]
        
        writer.writerow((date, description, notes, account, deposit, withdrawal, balance))
    
finally:
    for account_file in account_files:
        account_file.close()
    rabo_mut_file.close()
