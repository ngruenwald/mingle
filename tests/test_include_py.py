from mingle import mingle

from helpers.utils import compare_files
from helpers.settings import *


def test_include_py(capsys):
    input: list[str] = [FIXTURES_PATH + "/**/input*.py"]
    template: str = FIXTURES_PATH + "/template_01.py"
    reference = FIXTURES_PATH + "/reference_01.py"
    output: str = OUTPUT_PATH + "/output_01.py"
    mode: str = "include"
    style: str = "py"

    mingle(input, output, template, mode, style)
    assert compare_files(output, reference, capsys)
