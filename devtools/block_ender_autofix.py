import ast
import os

def safe_readlines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            return f.readlines()

def safe_write(file_path, lines):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except UnicodeEncodeError:
        with open(file_path, "w", encoding="latin-1") as f:
            f.writelines(lines)

def get_expected_comment(node):
    if isinstance(node, ast.FunctionDef):
        return f"# END {node.name}", node.body[-1].lineno
    elif isinstance(node, ast.If):
        return "# END if", node.body[-1].lineno
    elif isinstance(node, ast.For):
        return "# END for", node.body[-1].lineno
    elif isinstance(node, ast.While):
        return "# END while", node.body[-1].lineno
    elif isinstance(node, ast.Try):
        return "# END try", node.body[-1].lineno
    elif isinstance(node, ast.With):
        context_names = ", ".join(ast.unparse(ctx.context_expr) for ctx in node.items)
        return f"# END with {context_names.strip()}", node.body[-1].lineno
    elif isinstance(node, ast.ExceptHandler):
        if node.type:
            exc = ast.unparse(node.type)
        else:
            exc = "except"
        if node.name:
            exc += f" {node.name}"
        return f"# END {exc.strip()}", node.body[-1].lineno
    return None, None

def fix_cst001_comments(file_path):
    lines = safe_readlines(file_path)
    try:
        tree = ast.parse("".join(lines))
    except Exception as e:
        print(f"Skipping {file_path} due to parse error: {e}")
        return

    inserts = []

    for node in ast.walk(tree):
        expected_comment, line_num = get_expected_comment(node)
        if expected_comment is None:
            continue

        check_idx = line_num
        while check_idx < len(lines) and lines[check_idx].strip() == "":
            check_idx += 1

        if check_idx >= len(lines) or not lines[check_idx].strip().startswith("# END"):
            inserts.append((check_idx, expected_comment + "\n"))
        else:
            existing = lines[check_idx].strip()
            if existing != expected_comment:
                inserts.append((check_idx, expected_comment + "\n"))

    if inserts:
        for idx, text in reversed(inserts):  # Reverse to avoid shifting lines
            lines[idx:idx+1] = [text]
        safe_write(file_path, lines)
        print(f"Fixed CST001 comments in {file_path}")

def fix_all_cst001_in_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py"):
                path = os.path.join(dirpath, file)
                fix_cst001_comments(path)

if __name__ == "__main__":
    TARGET_DIR = "src"  # Adjust to your root Python source directory
    fix_all_cst001_in_directory(TARGET_DIR)
