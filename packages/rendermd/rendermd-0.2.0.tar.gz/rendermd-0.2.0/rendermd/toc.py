import difflib
from typing import List, Tuple

import md_toc

from .core import Diff, MarkdownGenerator

TOC_BLOCK = ("[//]: # (START_TOC)", "[//]: # (END_TOC)")


class TocGenerator(MarkdownGenerator):
    def generate_content(
        self, original_lines: List[str], file_path: str
    ) -> Tuple[str, Diff]:
        return generate_markdown_toc(original_lines, file_path)


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


def generate_markdown_toc(
    original_lines: List[str], file_path: str
) -> Tuple[str, Diff]:
    """Given a markdown file, generate table of contents.

    Returns:
        (content, diff)
    """
    resulted_lines = []

    start, end = TOC_BLOCK

    inside_toc_block = False
    contains_toc = False

    for line in original_lines:
        line = line.rstrip("\n")

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
