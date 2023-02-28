import os
import re

root_directory = r'/path'
# Define the regular expression patterns to match the line pattern and URLs
line_pattern = re.compile(r':')
url_pattern = re.compile(r'http|https')

# Traverse the directory tree and process each file
for root, dirs, files in os.walk(root_directory):
    for file_name in files:
        # Construct the full path to the file
        file_path = os.path.join(root, file_name)

        # Extract the file name without extension
        file_name_without_ext = os.path.splitext(file_name)[0]

        # Remove data within curly braces, square brackets or parentheses, as well as non-alphanumeric characters except dot and spaces using regular expression
        cleaned_file_name = re.sub(r'\(([^)]*)\)|\{([^}]*)\}|\[([^\]]*)\]|\s+', '', file_name_without_ext)

        # Add the file extension back to the cleaned file name
        cleaned_file_name_with_ext = cleaned_file_name + os.path.splitext(file_name)[1]

        # Rename the file
        os.rename(file_path, os.path.join(root, cleaned_file_name_with_ext))

        # Read the contents of the file
        with open(os.path.join(root, cleaned_file_name_with_ext), 'r', encoding="utf_8") as f:
            lines = f.readlines()

        # Remove lines that do not match the line pattern or contain URLs
        cleaned_lines = []
        for line in lines:
            if line_pattern.search(line) and not url_pattern.search(line):
                cleaned_line = line.strip()
                cleaned_lines.append(cleaned_line)
        
        # Write the cleaned lines back to a new file
        with open(os.path.join(root, cleaned_file_name_with_ext), 'w', encoding="utf_8") as f:
            f.write('\n'.join(cleaned_lines))