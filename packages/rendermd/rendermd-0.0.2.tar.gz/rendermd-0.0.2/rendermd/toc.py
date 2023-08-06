import difflib
from typing import Tuple

import md_toc

from .printer import Diff

TOC_BLOCK = ("[//]: # (START_TOC)", "[//]: # (END_TOC)")


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

    return (
        "\n".join(resulted_lines),
        contains_toc
        and Diff(list(difflib.context_diff(original_lines, resulted_lines)))
        or Diff([]),
    )
