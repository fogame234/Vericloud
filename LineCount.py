import os
import time

def count_lines_in_file(file_path):
    with open(file_path, "rb") as file:
        line_count = sum(buffer.count(b"\n") for buffer in iter(lambda: file.read(1024 * 1024), b""))
        return line_count

def count_lines_in_folder(folder_path):
    total_line_count = 0
    start_time = time.perf_counter()
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        line_count = count_lines_in_file(file_path)
        total_line_count += line_count
        print(f"{file_path} line count: {line_count}")
    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"Total line count: {total_line_count}")

source_folder = "/path/to/folder"
count_lines_in_folder(source_folder)
