import os

folder_path = r"/path"

for root, dirs, files in os.walk(folder_path):
    # Remove .sql and .csv files
    for filename in files:
        if filename.endswith(".sql") or filename.endswith(".csv"):
            file_path = os.path.join(root, filename)
            os.remove(file_path)
    
    # Rename directories with underscores
    for directory in dirs:
        if "_" in directory:
            new_dirname = directory.split("_")[0]
            old_dirpath = os.path.join(root, directory)
            new_dirpath = os.path.join(root, new_dirname)
            os.rename(old_dirpath, new_dirpath)