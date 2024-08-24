from mingle import mingle

from helpers.settings import *
from helpers.utils import compare_files


def test_exclude_py(capsys):
    input: list[str] = [FIXTURES_PATH + "/**/input*.py"]
    template: str = ""  # not required
    reference = FIXTURES_PATH + "/reference_02.py"
    output: str = OUTPUT_PATH + "/output_02.py"
    mode: str = "exclude"
    style: str = "py"

    mingle(input, output, template, mode, style)
    assert compare_files(output, reference, capsys)
