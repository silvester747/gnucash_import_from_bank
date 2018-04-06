from gnucash_import_converter.gnucash import GnuCashStatement, GnuCashCsvWriter

expected_header_row = "Date,Description,Notes,Account,Deposit,Withdrawal,Balance"
test_accounts = (
        "NL12RABO76575776",
        "NL54RABO73838738",
        )
test_statements = (
        GnuCashStatement(
            date="2018-02-23",
            num=12,
            description="Supermarket",
            notes="Debit card payment",
            account=test_accounts[0],
            deposit=0,
            withdrawal="12,23",
            balance="105,34"
            ),
        GnuCashStatement(
            date="2018-02-25",
            num=13,
            description="Pharmacy",
            notes="Pills",
            account=test_accounts[0],
            deposit=0,
            withdrawal="38,95",
            balance="70,12"
            ),
        GnuCashStatement(
            date="2018-02-15",
            num=13,
            description="Candystore",
            notes="Other pills",
            account=test_accounts[1],
            deposit=0,
            withdrawal="148,99",
            balance="-30,20"
            ),
        )
expected_csv_rows = (
        '2018-02-23,Supermarket,Debit card payment,NL12RABO76575776,0,"12,23","105,34"',
        '2018-02-25,Pharmacy,Pills,NL12RABO76575776,0,"38,95","70,12"',
        '2018-02-15,Candystore,Other pills,NL54RABO73838738,0,"148,99","-30,20"',
        )

def test_one_statement_written_to_one_file(tmpdir):
    writer = GnuCashCsvWriter(str(tmpdir))
    try:
        writer.write_statement(test_statements[0])
    finally:
        writer.close()

    expected_file = tmpdir.join(test_accounts[0] + ".csv")
    assert expected_file.check()

    expected_content = "\n".join((
            expected_header_row,
            expected_csv_rows[0],
            ""
            ))
    assert expected_file.read_text("latin1") == expected_content


def test_multiple_statements_written_to_one_file(tmpdir):
    writer = GnuCashCsvWriter(str(tmpdir))
    try:
        writer.write_statement(test_statements[0])
        writer.write_statement(test_statements[1])
    finally:
        writer.close()

    expected_file = tmpdir.join(test_accounts[0] + ".csv")
    assert expected_file.check()

    expected_content = "\n".join((
            expected_header_row,
            expected_csv_rows[0],
            expected_csv_rows[1],
            ""
            ))
    assert expected_file.read_text("latin1") == expected_content


def test_multiple_statements_written_to_multiple_files(tmpdir):
    writer = GnuCashCsvWriter(str(tmpdir))
    try:
        writer.write_statement(test_statements[0])
        writer.write_statement(test_statements[1])
        writer.write_statement(test_statements[2])
    finally:
        writer.close()

    expected_file = tmpdir.join(test_accounts[0] + ".csv")
    assert expected_file.check()

    expected_content = "\n".join((
            expected_header_row,
            expected_csv_rows[0],
            expected_csv_rows[1],
            ""
            ))
    assert expected_file.read_text("latin1") == expected_content

    expected_file = tmpdir.join(test_accounts[1] + ".csv")
    assert expected_file.check()

    expected_content = "\n".join((
            expected_header_row,
            expected_csv_rows[2],
            ""
            ))
    assert expected_file.read_text("latin1") == expected_content

