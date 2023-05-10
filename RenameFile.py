import os
import natsort
import re

source_folder = /path
pattern = r"^\d+_Combolist.txt$"

existing_files = [f for f in os.listdir(source_folder) if re.match(pattern, f)]

count = 1

for file in natsort.os_sorted(os.listdir(source_folder)):
    org = os.path.join(source_folder, file)
    new = os.path.join(source_folder, str(count) + "_Combolist" + ".txt")
    if file in existing_files:
        print(f"Skipping {file}")
        count += 1
    else:
        os.rename(org, new)
        count += 1
