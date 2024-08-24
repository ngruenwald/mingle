from mingle import mingle

from helpers.utils import compare_files
from helpers.settings import *


def test_include_cpp(capsys):
    input: list[str] = [FIXTURES_PATH + "/**/input*.cpp"]
    template: str = FIXTURES_PATH + "/template_01.cpp"
    reference = FIXTURES_PATH + "/reference_01.cpp"
    output: str = OUTPUT_PATH + "/output_01.cpp"
    mode: str = "include"
    style: str = "cpp"

    mingle(input, output, template, mode, style)
    assert compare_files(output, reference, capsys)
