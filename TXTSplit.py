import os
import io

INPUT_DIR = "/path"

def process_file(file_path):
    print(file_path)
    output_dir_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir_path = os.path.join(os.path.dirname(file_path), output_dir_name)
    os.makedirs(output_dir_path, exist_ok=True)

    with io.open(file_path , "r", encoding="Latin-1") as input_file:
        line_count = 0
        file_count = 0
        output_file = None
        
        for line in input_file:
            if line_count == 0:
                # If this is the first line, create a new output file
                file_count += 1
                output_file_path = os.path.join(output_dir_path, f"{output_dir_name}_{file_count}.txt")
                output_file = io.open(output_file_path, "w", encoding="Latin-1")
            
            output_file.write(line)
            line_count += 1
            
            if line_count == 500:
                # If we've reached the line limit, close the current output file
                output_file.close()
                output_file = None
                line_count = 0
                
        # If there are any remaining lines, write them to a final output file
        if output_file is not None:
            output_file.close()

    os.remove(file_path)
def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                process_file(file_path)

if __name__ == "__main__":
    process_folder(INPUT_DIR)
