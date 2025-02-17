import os

def count_lines_in_py_files(directory):
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = sum(1 for _ in f)
                    print(f"{file}: {lines} Zeilen")
                    total_lines += lines
    print(f"\nGesamtanzahl Zeilen: {total_lines}")

# Pfad zum Projektordner hier anpassen:
count_lines_in_py_files("../src")
