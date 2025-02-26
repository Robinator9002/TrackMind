"""
This is an external file, not used in the project, just to calculate the projects size.
IMPORTANT: Delete this file before finishing the Project!!!
"""

import ast
import os


def count_lines_in_py_files(directory, exclude_folders=None):
    total_lines = 0
    total_functions = 0
    total_classes = 0
    total_files = 0

    if exclude_folders is None:
        exclude_folders = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_folders]  # Exclude folders

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                total_files += 1

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    file_lines = len(lines)
                    total_lines += file_lines

                    code = ""
                    for line in lines:
                        code += line

                    tree = ast.parse(code)
                    file_functions = 0
                    file_classes = 0
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            file_functions += 1
                        elif isinstance(node, ast.ClassDef):
                            file_classes += 1

                    total_functions += file_functions
                    total_classes += file_classes

                    print(f"{file}:")
                    print(f"- Lines: {file_lines}")
                    print(f"- Functions: {file_functions}")
                    print(f"- Classes: {file_classes}")

    print(f"\nTotal lines of code: {total_lines}")
    print(f"Total functions: {total_functions}")
    print(f"Total classes: {total_classes}")
    print(f"Total files: {total_files}")


def count_docstrings_and_functions_length(directory, exclude_folders=None):
    total_docstrings_length = 0
    total_docstrings_count = 0
    total_functions_length = 0
    total_functions_count = 0

    if exclude_folders is None:
        exclude_folders = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_folders]  # Exclude folders

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    code = ""
                    for line in lines:
                        code += line

                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                            docstring = node.value.s
                            total_docstrings_length += len(docstring)
                            total_docstrings_count += 1

                        if isinstance(node, ast.FunctionDef):
                            function_length = len(node.body)
                            total_functions_length += function_length
                            total_functions_count += 1

    print(f"\nTotal docstring length: {total_docstrings_length} (letters)")
    print(f"Total docstrings count: {total_docstrings_count}")
    print(f"Total function length: {total_functions_length} (letters)")
    print(f"Total functions count: {total_functions_count}")

def find_functions_without_docstrings(directory, exclude_folders=None):
    functions_without_docstrings = []

    if exclude_folders is None:
        exclude_folders = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_folders]  # Exclude folders

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    code = ""
                    for line in lines:
                        code += line

                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and not any(isinstance(child, ast.Expr) and isinstance(child.value, ast.Str) for child in node.body):
                            function_name = node.name
                            function_lineno = node.lineno
                            functions_without_docstrings.append((file_path, function_name, function_lineno))

    print("\nFunctions without docstrings:")
    for file_path, function_name, function_lineno in functions_without_docstrings:
        print(f"{file_path}:{function_lineno} - {function_name}")


count_lines_in_py_files("../TrackMind", exclude_folders=[".venv"])
count_docstrings_and_functions_length("../TrackMind", exclude_folders=[".venv"])
find_functions_without_docstrings("../TrackMind", exclude_folders=[".venv"])
