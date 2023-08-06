import glob
from typing import List

from .command_parser import parse_command_line
from .printer import Printer
from .toc import generate_markdown_toc


def get_mardown_files(patterns: List[str], recursive: bool) -> List[str]:
    files = []
    for pattern in patterns:
        files += glob.glob(pattern, recursive=bool(recursive))

    return files


def rewrite_markdown(file_path: str) -> None:
    file_content, diff = generate_markdown_toc(file_path)
    if diff:
        print(f"Generating {file_path} ...")
        Printer.print_colored_diff(diff)

        with open(file_path, "w") as outfile:
            print(file_content, file=outfile)


def main() -> None:
    opts = parse_command_line()
    for markdown_file in get_mardown_files(opts.patterns, opts.recursive):
        rewrite_markdown(markdown_file)

    print(f"{__file__} done!")


if __name__ == "__main__":
    main()
