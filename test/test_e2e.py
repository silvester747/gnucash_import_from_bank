import os
import subprocess
import shutil

def test_full_import(tmpdir):
    """
    Test full script run.
    """
    input_csv = os.path.join(os.path.dirname(__file__), "rabobank.csv")
    assert os.path.isfile(input_csv)
    shutil.copy(input_csv, tmpdir)

    script = os.path.join(os.path.dirname(__file__), "..", "gnucash_import_from_bank.py")
    assert os.path.isfile(script)

    assert subprocess.call("{} {}".format(script, tmpdir.join("rabobank.csv")),
                           cwd=str(tmpdir),
                           shell=True) == 0

    out_csv = tmpdir.join("NL12RABO1234567890.csv")
    assert out_csv.check()

    expected_content = """Date,Description,Notes,Account,Deposit,Withdrawal,Balance
2018-02-28,Computershop (987654321),Nice computer stuff ,NL12RABO1234567890,0,"148,99","419,84"
"""
    assert out_csv.read_text("latin1") == expected_content

