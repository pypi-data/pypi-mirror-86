import argparse
from dataclasses import dataclass
import difflib
from enum import Enum
import glob
from typing import List, NewType, Tuple

import md_toc

TOC_BLOCK = ("[//]: # (START_TOC)", "[//]: # (END_TOC)")

Diff = NewType("Diff", List[str])


class Printer(Enum):
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    RED = FAIL = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def print(self, msg: str) -> None:
        print(self.value, msg, Printer.RESET.value)


def print_colored_diff(diff: Diff) -> None:
    for line in diff:
        if line.startswith("+"):
            Printer.GREEN.print(line)
        elif line.startswith("!"):
            Printer.WARNING.print(line)
        elif line.startswith("-") and not line.startswith("---"):
            Printer.RED.print(line)
        elif line.startswith("^"):
            Printer.BLUE.print(line)
        else:
            print(line)


@dataclass
class CommandLineOptions:
    patterns: List[str]
    recursive: bool


def get_mardown_files(patterns: List[str], recursive: bool) -> List[str]:
    files = []
    for pattern in patterns:
        files += glob.glob(pattern, recursive=bool(recursive))

    return files


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Populate Table of Contents in markdown files."
    )
    parser.add_argument(
        "-p",
        "--pattern",
        dest="patterns",
        default="**/README.md",
        help="Comma separated list of markdown files to populate",
    )
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do not search for files recursively",
    )
    return parser


def get_toc(file_path: str) -> str:
    table_of_contents = md_toc.build_toc(file_path, parser="redcarpet")
    return "\n".join(
        [
            TOC_BLOCK[0],
            "Table of Contents",
            "=================",
            table_of_contents,
            TOC_BLOCK[1],
        ]
    )


def generate_markdown_toc(file_path: str) -> Tuple[str, Diff]:
    """Given a markdown file, generate table of contents.

    Returns:
        (content, diff)
    """
    with open(file_path) as infile:
        original_lines = []
        resulted_lines = []

        start, end = TOC_BLOCK

        inside_toc_block = False
        contains_toc = False

        for line in infile.readlines():
            line = line.rstrip("\n")
            original_lines.append(line)

            if line.startswith(start):
                inside_toc_block = True
                contains_toc = True
                resulted_lines += get_toc(file_path).splitlines()
            elif line.startswith(end):
                inside_toc_block = False
                continue

            if not inside_toc_block:
                resulted_lines.append(line)

    # if contains_toc:
    #     breakpoint()
    return (
        "\n".join(resulted_lines),
        contains_toc
        and Diff(list(difflib.context_diff(original_lines, resulted_lines)))
        or Diff([]),
    )


def rewrite_markdown(file_path: str) -> None:
    file_content, diff = generate_markdown_toc(file_path)
    if diff:
        print(f"Generating {file_path} ...")
        print_colored_diff(diff)

        with open(file_path, "w") as outfile:
            print(file_content, file=outfile)


def parse_command_line() -> CommandLineOptions:
    parser = get_parser()
    options = parser.parse_args()
    return CommandLineOptions(
        patterns=options.patterns.split(","), recursive=options.recursive
    )


def main() -> None:
    opts = parse_command_line()
    for markdown_file in get_mardown_files(opts.patterns, opts.recursive):
        rewrite_markdown(markdown_file)

    print(f"{__file__} done!")


if __name__ == "__main__":
    main()
