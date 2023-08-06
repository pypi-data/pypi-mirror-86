from typing import List, NewType, Tuple

Diff = NewType("Diff", List[str])


class MarkdownGenerator:
    def generate_content(
        self, original_lines: List[str], file_path: str
    ) -> Tuple[str, Diff]:
        raise NotImplementedError()
