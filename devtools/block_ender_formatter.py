# devtools/__init__.py
"""
Development tools package initializer.
This package contains custom development-time tools such as formatters,
linters, and Flake8 plugins.
"""

# No specific code needed here yet, but this makes devtools a proper Python package.

# devtools/block_ender_formatter.py
import os
import re
import sys
from pathlib import Path

RULES = {
    "if": r"(?<!# END IF)$",
    "for": r"(?<!# END FOR)$",
    "while": r"(?<!# END WHILE)$",
    "def": r"(?<!# END DEF)$",
    "with": r"(?<!# END WITH)$",
}

BLOCK_KEYWORDS = list(RULES.keys())


def safe_readlines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            return f.readlines()


def safe_writelines(file_path, lines):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except UnicodeEncodeError:
        with open(file_path, "w", encoding="latin-1") as f:
            f.writelines(lines)


def check_block_enders(file_path):
    suggestions = []
    lines = safe_readlines(file_path)
    for i, line in enumerate(lines):
        for keyword in BLOCK_KEYWORDS:
            if re.match(rf"^\s*{keyword}\b", line) and not re.search(RULES[keyword], line):
                suggestions.append((i + 1, keyword, line.strip()))
    return suggestions


def dry_run(file_path):
    suggestions = check_block_enders(file_path)
    if suggestions:
        print(f"\n[!] Suggestions for {file_path}:")
        for line_num, keyword, line in suggestions:
            print(f"  Line {line_num}: '{line}' → should end with '# END {keyword.upper()}'")
    else:
        print(f"[✓] {file_path} is compliant.")


def apply_format(file_path):
    lines = safe_readlines(file_path)
    new_lines = []
    for line in lines:
        for keyword in BLOCK_KEYWORDS:
            if re.match(rf"^\s*{keyword}\b", line) and not re.search(RULES[keyword], line):
                line = line.rstrip() + f"  # END {keyword.upper()}\n"
                break
        new_lines.append(line)
    safe_writelines(file_path, new_lines)
    print(f"[✓] Formatted {file_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BlockEnder Formatter")
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument("--format", action="store_true", help="Apply formatting fixes")
    args = parser.parse_args()

    target = Path(args.path)
    files = (
        [target]
        if target.is_file() and target.suffix == ".py"
        else list(target.rglob("*.py"))
    )

    for f in files:
        if args.format:
            apply_format(f)
        else:
            dry_run(f)


if __name__ == "__main__":
    main()
