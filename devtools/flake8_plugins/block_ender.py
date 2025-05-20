import ast
import re
from typing import Generator, Tuple


class BlockEnder:
    """Custom flake8 plugin to check for end comments and blank lines between functions."""
    name = "flake8-block-ender"
    version = "0.1.0"

    def __init__(self, tree, lines):
        self.tree = tree
        self.lines = lines

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        yield from self._check_end_comments()
        yield from self._check_blank_lines_between_functions()

    def _check_end_comments(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                block_type = node.name
                end_lineno = node.body[-1].lineno
                expected_comment = f"# END {block_type}"

            elif isinstance(node, ast.If):
                block_type = "if"
                end_lineno = node.body[-1].lineno
                expected_comment = f"# END {block_type}"

            elif isinstance(node, ast.While):
                block_type = "while"
                end_lineno = node.body[-1].lineno
                expected_comment = f"# END {block_type}"

            elif isinstance(node, ast.For):
                block_type = "for"
                end_lineno = node.body[-1].lineno
                expected_comment = f"# END {block_type}"

            elif isinstance(node, ast.With):
                block_type = "with " + ", ".join(
                    self._get_source_segment(context) for context in node.items
                )
                end_lineno = node.body[-1].lineno
                expected_comment = f"# END {block_type.strip()}"

            elif isinstance(node, ast.Try):
                end_lineno = node.body[-1].lineno
                expected_comment = "# END try"

            elif isinstance(node, ast.ExceptHandler):
                if node.type:
                    try:
                        exc = self._get_source_segment(node.type)
                    except Exception:
                        exc = "except"
                else:
                    exc = "except"
                if node.name:
                    exc += f" {node.name}"
                end_lineno = node.body[-1].lineno
                expected_comment = f"# END {exc.strip()}"

            else:
                continue

            # Now check if expected comment exists after the block
            comment_line_idx = end_lineno
            while comment_line_idx < len(self.lines):
                line = self.lines[comment_line_idx].strip()
                if line:
                    if not line.startswith(expected_comment):
                        yield (
                            comment_line_idx + 1,
                            0,
                            f"CST001 Missing or incorrect end comment '{expected_comment}'",
                            type(self),
                        )
                    break
                comment_line_idx += 1

    def _get_source_segment(self, node):
        """Try to get readable source of a node if available."""
        return ast.unparse(node) if hasattr(ast, 'unparse') else "<expr>"

    def _check_blank_lines_between_functions(self):
        func_line_numbers = [
            node.lineno for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)
        ]
        func_line_numbers.sort()

        for i in range(1, len(func_line_numbers)):
            prev_func_end = func_line_numbers[i - 1]
            curr_func_start = func_line_numbers[i]
            blank_lines = 0
            for lineno in range(prev_func_end, curr_func_start - 1):
                if self.lines[lineno].strip() == "":
                    blank_lines += 1

            if blank_lines != 2:
                yield (
                    curr_func_start,
                    0,
                    f"CST002 Expected 2 blank lines between functions, found {blank_lines}",
                    type(self),
                )
