import difflib
import filecmp

from mingle import mingle

FIXTURES_PATH = "tests/fixtures"
OUTPUT_PATH = "tests/output"


def print_diff(file1: str, file2: str) -> None:
    with open(file1) as f1:
        d1 = f1.readlines()
    with open(file2) as f2:
        d2 = f2.readlines()
    for line in difflib.unified_diff(d1, d2, fromfile=file1, tofile=file2, lineterm=""):
        print(line)


def compare_files(file1: str, file2: str, capsys) -> bool:
    res = filecmp.cmp(file1, file2)
    if not res:
        with capsys.disabled():
            print_diff(file1, file2)
    return res


def test_mingle_01(capsys):
    input: list[str] = [FIXTURES_PATH + "/**/input*.py"]
    template: str = FIXTURES_PATH + "/template_01.py"
    reference = FIXTURES_PATH + "/reference_01.py"
    output: str = OUTPUT_PATH + "/output_01.py"
    mode: str = "include"
    style: str = "py"

    mingle(input, output, template, mode, style)
    assert compare_files(output, reference, capsys)


def test_mingle_02(capsys):
    input: list[str] = [FIXTURES_PATH + "/**/input*.py"]
    template: str = ""  # not required
    reference = FIXTURES_PATH + "/reference_02.py"
    output: str = OUTPUT_PATH + "/output_02.py"
    mode: str = "exclude"
    style: str = "py"

    mingle(input, output, template, mode, style)
    assert compare_files(output, reference, capsys)
