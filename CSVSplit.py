import os
import csv

INPUT_DIR = /path

def process_file(file_path):
    output_dir_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir_path = os.path.join(os.path.dirname(file_path), output_dir_name)
    os.makedirs(output_dir_path, exist_ok=True)

    with open(file_path, "r", newline='', encoding="utf-8") as input_file:
        csv_reader = csv.reader(input_file)
        header = next(csv_reader)
        row_count = 0
        file_count = 0
        output_file = None

        for row in csv_reader:
            if row_count == 0:
                # If this is the first row, create a new output file
                file_count += 1
                output_file_path = os.path.join(output_dir_path, f"{output_dir_name}_{file_count}.csv")
                output_file = open(output_file_path, "w", newline='', encoding="utf-8")
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(header)

            csv_writer.writerow(row)
            row_count += 1

            if row_count == 500:
                # If we've reached the row limit, close the current output file
                output_file.close()
                output_file = None
                row_count = 0

        # If there are any remaining rows, write them to a final output file
        if output_file is not None:
            output_file.close()

def process_folder(folder_path):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(".csv"):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path)

if __name__ == "__main__":
    process_folder(INPUT_DIR)
