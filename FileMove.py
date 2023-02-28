import os
import shutil
from pathlib import Path
from tkinter import filedialog, Tk
from alive_progress import alive_bar

progress_bar = lambda: alive_bar(title="Moving files")

source_folder = Path(filedialog.askdirectory())
extension = [".csv", ".xlsx", ".xls", ".sql"]


def get_new_file_name(file_name, duplicate_num):
    if duplicate_num == 0:
        return file_name

    stem, ext = os.path.splitext(file_name)
    return f"{stem}_{duplicate_num}{ext}"


def move_file(source, dest, file_name, duplicate_num=0):
    new_name = get_new_file_name(file_name, duplicate_num)
    new_path = dest / new_name

    if new_path.exists():
        move_file(source, dest, file_name, duplicate_num + 1)
    else:
        src_path = source / file_name
        shutil.move(src_path, new_path)


with progress_bar() as bar:
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            bar()

            src_path = Path(root) / file_name
            rel_path = src_path.relative_to(source_folder)

            if src_path.suffix not in extension:
                dest = source_folder / "_NO_PASSWORDS" / rel_path
            elif "_" in root:
                continue
            elif src_path.suffix == ".sql":
                dest = Path("/path/to/folder") / rel_path
            else:
                dest = Path("/path/to/folder") / rel_path

            if src_path.is_file():
                parent_dir = src_path.parent
                if parent_dir == source_folder:
                    move_file(parent_dir, dest, file_name)
                    print(f"Moved file: {file_name}")
                    continue

            dest.parent.mkdir(parents=True, exist_ok=True)
            move_file(src_path.parent, dest.parent, file_name)
            print(f"Moved file: {file_name}")

            if not os.listdir(src_path.parent):
                os.rmdir(src_path.parent)
                print(f"Removed empty directory: {src_path.parent}")
