# coding=utf-8
import locale
locale.setlocale(locale.LC_ALL, "")

from gnucash_import_converter.rabobank import RabobankCsvReader

header_row = """IBAN/BBAN,Munt,BIC,Volgnr,Datum,Rentedatum,Bedrag,Saldo na trn,Tegenrekening IBAN/BBAN,Naam tegenpartij,Naam uiteindelijke partij,Naam initiërende partij,BIC tegenpartij,Code,Batch ID,Transactiereferentie,Machtigingskenmerk,Incassant ID,Betalingskenmerk,Omschrijving-1,Omschrijving-2,Omschrijving-3,Reden retour,Oorspr bedrag,Oorspr munt,Koers"""

def test_import_single_line(tmpdir):
    input_transaction = """NL12RABO1234567890,EUR,RABONL2U,4129,2018-02-28,2018-02-29,"-148,99","419,84",987654321,Computershop,,,,db,,,,,,Nice computer stuff,,,,,,"""

    input_file = tmpdir.join("input.csv")
    input_file.write_text("\n".join((header_row, input_transaction, "")),
                          encoding="latin-1",
                          ensure=True)

    reader = RabobankCsvReader(str(input_file))
    try:
        statements = list(reader)
    finally:
        reader.close()

    assert len(statements) == 1
    assert statements[0].date == "2018-02-28"
    assert statements[0].num == "4129"
    assert statements[0].description == "Computershop (987654321)"
    assert statements[0].notes == "Nice computer stuff"
    assert statements[0].account == "NL12RABO1234567890"
    assert statements[0].deposit == 0
    assert statements[0].withdrawal == "148,99"
    assert statements[0].balance == "419,84"

