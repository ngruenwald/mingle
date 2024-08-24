import difflib
import filecmp


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