# coding=utf-8
import locale
locale.setlocale(locale.LC_ALL, "")

from gnucash_import_converter.abnamro import AbnAmroTxtReader


def test_sepa_withdrawal(tmpdir):
    input_transaction = """123456789	EUR	20161008	1728,69	1028,69	20161008	-700,00	SEPA Overboeking                 IBAN: NL32INGB0083736388        BIC: INGBNL2A                    Naam: Piet Pardoes          Omschrijving: Trui                                               """

    input_file = tmpdir.join("input.csv")
    input_file.write_text("\n".join((input_transaction, "")),
                          encoding="utf-8",
                          ensure=True)

    reader = AbnAmroTxtReader(str(input_file))
    try:
        statements = list(reader)
    finally:
        reader.close()

    assert len(statements) == 1
    assert statements[0].date == "2016-10-08"
    assert statements[0].num is None
    assert statements[0].description == "Piet Pardoes (NL32INGB0083736388)"
    assert statements[0].notes == "Trui"
    assert statements[0].account == "123456789"
    assert statements[0].deposit == 0
    assert statements[0].withdrawal == 700.00
    assert statements[0].balance == 1028.69


def test_sepa_deposit(tmpdir):
    input_transaction = """837363836	EUR	20161223	429,20	2639,63	20161223	1250,43	SEPA Overboeking                 IBAN: NL87INGB0876467578        BIC: INGBNL2A                    Naam: My sugardaddy                             Omschrijving: Money money money                              Kenmerk: 201612543463243fd323452"""

    input_file = tmpdir.join("input.csv")
    input_file.write_text("\n".join((input_transaction, "")),
                          encoding="utf-8",
                          ensure=True)

    reader = AbnAmroTxtReader(str(input_file))
    try:
        statements = list(reader)
    finally:
        reader.close()

    assert len(statements) == 1
    assert statements[0].date == "2016-12-23"
    assert statements[0].num is None
    assert statements[0].description == "My sugardaddy (NL87INGB0876467578)"
    assert statements[0].notes == "Money money money"
    assert statements[0].account == "837363836"
    assert statements[0].deposit == 1250.43
    assert statements[0].withdrawal == 0
    assert statements[0].balance == 2639.63


def test_bea_withdrawal(tmpdir):
    input_transaction = """874532457	EUR	20161011	1028,69	998,13	20161011	-30,56	BEA   NR:IP477P   11.10.16/10.54 PharmaKing 7803 AMSTERDAM,PAS476     """

    input_file = tmpdir.join("input.csv")
    input_file.write_text("\n".join((input_transaction, "")),
                          encoding="utf-8",
                          ensure=True)

    reader = AbnAmroTxtReader(str(input_file))
    try:
        statements = list(reader)
    finally:
        reader.close()

    assert len(statements) == 1
    assert statements[0].date == "2016-10-11"
    assert statements[0].num is None
    assert statements[0].description == "PharmaKing 7803 AMSTERDAM"
    assert statements[0].notes == None
    assert statements[0].account == "874532457"
    assert statements[0].deposit == 0
    assert statements[0].withdrawal == 30.56
    assert statements[0].balance == 998.13


def test_bea_withdrawal2(tmpdir):
    input_transaction = """512345543	EUR	20180626	4459,24	4408,24	20180626	-51,00	BEA   NR:CT535434 26.06.18/12.08 CCV*Olaf Van Verde OEGST,PAS232 """

    input_file = tmpdir.join("input.csv")
    input_file.write_text("\n".join((input_transaction, "")),
                          encoding="utf-8",
                          ensure=True)

    reader = AbnAmroTxtReader(str(input_file))
    try:
        statements = list(reader)
    finally:
        reader.close()

    assert len(statements) == 1
    assert statements[0].date == "2018-06-26"
    assert statements[0].num is None
    assert statements[0].description == "CCV*Olaf Van Verde OEGST"
    assert statements[0].notes == None
    assert statements[0].account == "512345543"
    assert statements[0].deposit == 0
    assert statements[0].withdrawal == 51.00
    assert statements[0].balance == 4408.24

def test_sepa_deposit_slash(tmpdir):
    input_transaction = """512345543	EUR	20181025	897,61	2420,36	20181025	1522,75	/TRTP/SEPA OVERBOEKING/IBAN/NL44INGB7394748399/BIC/INGBNL2A/NAME/My Fantastic Job BV/REMI/Salaris Oktober 2018/EREF/20183234234324-234326/3                                           """

    input_file = tmpdir.join("input.csv")
    input_file.write_text("\n".join((input_transaction, "")),
                          encoding="utf-8",
                          ensure=True)

    reader = AbnAmroTxtReader(str(input_file))
    try:
        statements = list(reader)
    finally:
        reader.close()

    assert len(statements) == 1
    assert statements[0].date == "2018-10-25"
    assert statements[0].num is None
    assert statements[0].description == "My Fantastic Job BV (NL44INGB7394748399)"
    assert statements[0].notes == "Salaris Oktober 2018"
    assert statements[0].account == "512345543"
    assert statements[0].deposit == 1522.75
    assert statements[0].withdrawal == 0
    assert statements[0].balance == 2420.36
