import os
import shutil

from gnucash_import_converter.main import main

def test_full_import(tmpdir):
    """
    Import a simple transactions file in Rabobank CSV format.
    """
    input_csv = os.path.join(os.path.dirname(__file__), "rabobank.csv")
    assert os.path.isfile(input_csv)
    shutil.copy(input_csv, tmpdir)

    argv = [
        "--type", "rabobank",
        str(tmpdir.join("rabobank.csv")),
    ]
    with tmpdir.as_cwd():
        main(argv)

    out_csv = tmpdir.join("NL12RABO1234567890.csv")
    assert out_csv.check()

    expected_content = """Date,Description,Notes,Account,Deposit,Withdrawal,Balance
2018-02-28,Computershop (987654321),Nice computer stuff ,NL12RABO1234567890,"0,00","148,99","419,84"
"""
    assert out_csv.read_text("latin1") == expected_content


def test_import_to_custom_output_directory(tmpdir):
    input_csv = os.path.join(os.path.dirname(__file__), "rabobank.csv")
    assert os.path.isfile(input_csv)
    shutil.copy(input_csv, tmpdir)

    output_dir = tmpdir.join('my_custom_output_dir')

    argv = [
        "--output_dir", str(output_dir),
        "--type", "rabobank",
        str(tmpdir.join("rabobank.csv")),
    ]
    with tmpdir.as_cwd():
        main(argv)

    out_csv = output_dir.join("NL12RABO1234567890.csv")
    assert out_csv.check()

    expected_content = """Date,Description,Notes,Account,Deposit,Withdrawal,Balance
2018-02-28,Computershop (987654321),Nice computer stuff ,NL12RABO1234567890,"0,00","148,99","419,84"
"""
    assert out_csv.read_text("latin1") == expected_content

