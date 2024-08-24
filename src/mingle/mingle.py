#!/usr/bin/env python3

import argparse
import glob
import regex


class Style:
    def __init__(
            self,
            block_beg: str,
            block_end: str,
            block_ins: str,
            comment_file: str,
            comment_file_line: str,
            ):
        self.block_beg = regex.compile(block_beg)
        self.block_end = regex.compile(block_end)
        self.block_ins = regex.compile(block_ins)
        self.comment_file = comment_file
        self.comment_file_line = comment_file_line


STYLES = {
    "c": Style(
        block_beg = "^\\s*/\\*\\s*>>\\s*(.*)\\*/$",
        block_end = "^\\s*/\\*\\s*<<\\s*(.*)\\*/$",
        block_ins = "^\\s*/\\*\\s*\\$\\$\\s*(.*)\\*/$",
        comment_file      = "/\\* source: {} \\*/\n",
        comment_file_line = "/\\* source: {}:{} \\*/\n",
    ),
    "cpp": Style(
        block_beg = "^\\s*//\\s*>>\\s*(.*)$",
        block_end = "^\\s*//\\s*<<\\s*(.*)$",
        block_ins = "^\\s*//\\s*\\$\\$\\s*(.*)$",
        comment_file      = "// source: {}\n",
        comment_file_line = "// source: {}:{}\n",
    ),
    "py": Style(
        block_beg = "^\\s*#\\s*>>\\s*(.*)$",
        block_end = "^\\s*#\\s*<<\\s*(.*)$",
        block_ins = "^\\s*#\\s*\\$\\$\\s*(.*)$",
        comment_file      = "# source: {}\n",
        comment_file_line = "# source: {}:{}\n",
    ),
}


def main():
    parser = argparse.ArgumentParser(prog="Mingle", description="Combine multiple files into one")
    parser.add_argument("-i", "--input", default=["*.py"], nargs="+", help="Input file (pattern)")
    parser.add_argument("-o", "--output", default="output.py", help="Output file")
    parser.add_argument("-t", "--template", default="template.py", help="Template file")
    parser.add_argument("-m", "--mode", default="include", choices=["include", "exclude"], help="Merge mode")
    parser.add_argument("-s", "--style", default="py", choices=["c", "cpp", "py"], help="Comment style")
    args = parser.parse_args()
    mingle(args.input, args.output, args.template, args.mode, args.style)


def mingle(input: list[str], output: str, template: str, mode: str, style_name: str) -> None:
    style = STYLES[style_name]
    data = {}
    gather_input_data(input, data, mode, style)
    if mode == "include":
        create_output_file(output, template, data, style)
    elif mode == "exclude":
        create_simple_output_file(output, data)


def gather_input_data(input_files: list[str], data: dict, mode: str, style: Style) -> None:
    for input_file in input_files:
        files = glob.glob(input_file, recursive=True)
        files.sort()
        for file in files:
            extract_data_from_file(file, data, mode, style)


def extract_data_from_file(input_file: str, data: dict, mode: str, style: Style) -> None:
    print(f"processing '{input_file}'")
    if mode == "exclude":
        extract_data_from_file_exclude(input_file, data, style)
    elif mode == "include":
        extract_data_from_file_include(input_file, data, style)
    else:
        print(f"invalid mode '{mode}'")


def extract_data_from_file_include(input_file: str, data: dict, style: Style) -> None:
    with open(input_file, "rt") as f:
        block_name: str = ""
        block_data: list[str] = []
        line_number: int = 0
        while True:
            line = f.readline()
            if not line:
                if block_name:
                    print(f"WARN: eol while in block '{block_name}'")
                break
            line_number += 1
            if block_name:
                # inside a block, check for blockend
                m = style.block_end.match(line)
                if m:
                    # TBD: should we verify the block name?
                    if block_name in data:
                        data[block_name].append("\n")
                        data[block_name].extend(block_data)
                    else:
                        data[block_name] = block_data
                    block_name = ""
                else:
                    block_data.append(line)
            else:
                # outside of block, check for block start
                m = style.block_beg.match(line)
                if m:
                    block_name = m.group(1).strip()
                    block_data = [style.comment_file_line.format(input_file, line_number)]


def extract_data_from_file_exclude(input_file: str, data: dict, style: Style) -> None:
    with open(input_file, "rt") as f:
        block_name: str = ""
        block_data: list[str] = []
        line_number: int = 0
        while True:
            line = f.readline()
            if not line:
                if block_name:
                    print(f"WARN: eol while in block '{block_name}'")
                break
            line_number += 1
            if block_name:
                # inside of block, check for block end
                m = style.block_end.match(line)
                if m:
                    block_name = ""
            else:
                # outside a block, check for block start
                m = style.block_beg.match(line)
                if m:
                    block_name = m.group(1).strip()
                else:
                    block_data.append(line)
        if block_data:
            if not "" in data:
                data[""] = []
            data[""].append("\n")
            data[""].append(style.comment_file.format(input_file))
            data[""].extend(block_data)


def create_output_file(output_file: str, template_file: str, data: dict, style: Style) -> None:
    output_data = []
    used_blocks = []
    with open(template_file, "rt") as f:
        while True:
            line = f.readline()
            if not line:
                break
            m = style.block_ins.match(line)
            if not m:
                output_data.append(line)
                continue
            block_name = m.group(1).strip()
            if not block_name in data:
                print(f"WARN: block '{block_name}' does not exist")
                continue
            output_data.extend(data[block_name])
            used_blocks.append(block_name)
    with open(output_file, "wt") as f:
        f.writelines(output_data)
    unused_blocks = set(data.keys()) - set(used_blocks)
    if unused_blocks:
        print(f"WARN: unused blocks: {unused_blocks}")


def create_simple_output_file(output_file: str, data: dict) -> None:
    with open(output_file, "wt") as f:
        for _, lines in data.items():
            f.writelines(lines)


if __name__ == "__main__":
    main()
