import os
from pathlib import Path
import pandas as pd
from alive_progress import alive_bar
import tkinter
import shutil

# Location Paths
fileWindow = tkinter.Tk()
fileWindow.withdraw()
source_folder = "/path"
dest_folder = "/path"
fix_folder = "/path"

patterns = [
    "email",
    "username",
    "password",
    "salt",
    "phone",
    "altphone",
    "firstname",
    "lastname",
    "address",
    "unit",
    "state",
    "zipcode",
    "creditcard",
    "passwport",
    "ssn"
]


def get_new_file_name(file_name, duplicate_num):
    # handle degenerate case of 0
    if duplicate_num == 0:
        return file_name

    # Split the path into the file stem and the extension
    # Docs for os.path.splitext: https://docs.python.org/3/library/os.path.html#os.path.splitext
    stem, ext = os.path.splitext(file_name)

    # Concatenate the duplicate num w/ file stem and add ext
    # For example file.txt with duplicate_num of 3 would become file_3.txt
    return stem + "_" + str(duplicate_num) + ext


def move_file(source_folder, dest_folder, file_name, duplicate_num=0):
    new_file_name = get_new_file_name(file_name, duplicate_num)
    if os.path.exists(os.path.join(dest_folder, new_file_name)):
        move_file(source_folder, dest_folder, file_name, duplicate_num + 1)
    else:
        src_file = os.path.join(source_folder, file_name)
        dst_file = os.path.join(dest_folder, new_file_name)
        shutil.move(src_file, dst_file)


progress_bar = lambda: alive_bar(title="Creating password file:")
with progress_bar() as bar:
    for root, dir, files in os.walk(source_folder):
        for fn in files:
            bar()
            src_path = Path(root).joinpath(fn)
            stem, ext = os.path.splitext(fn)
            parent_path = Path(dest_folder).joinpath(stem)
            rel_path = os.path.relpath(src_path, source_folder)
            dest_path = Path(dest_folder).joinpath(rel_path)
            fix_path = Path(fix_folder).joinpath(rel_path)

            try:
                df = pd.read_csv(
                    rf"{src_path}",
                    header=0,
                    sep=",",
                    on_bad_lines="skip",
                    encoding_errors="replace",
                    dtype="str",
                )
            except Exception as e:
                fix_path.parent.mkdir(parents=True, exist_ok=True)
                print(f"Problem file: {fn} caused Exception: {e}")
                move_file(src_path.parent, fix_path.parent, fn)
                continue
            df.columns = [x.lower() for x in df.columns]
            headers = df.columns

            # Header variable reset
            email = ""
            password = ""
            username = ""
            phone = ""
            salt = ""
            altphone = ""

            headers = [x.lower() for x in headers]

            for header in headers:
                for pattern in patterns:
                    if pattern == header:
                        if header == "email":
                            email = header
                        if header == "password":
                            password = header
                        if header == "username":
                            username = header
                        if header == "salt":
                            salt = header
                        if header == "phone":
                            phone = header
                        if header == "altphone":
                            altphone = header
            try:
                if not email and not password and not username and not phone and not altphone:
                    print(f"File {fn} cannot be processed")
                    fix_path.parent.mkdir(parents=True, exist_ok=True)
                    move_file(src_path.parent, fix_path.parent, fn)

                if email in headers:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    comboUser = df[email] + ":" + df[password]
                    with open(
                        f"{dest_path.parent}\{stem}_email.txt", "w", encoding="utf_8"
                    ) as fp:
                        for line in comboUser:
                            if (
                                not str(line).__contains__("nan")
                                and not str(line).__contains__("<blank>")
                                and not str(line).__contains__("?")
                                and not str(line).__contains__("Empty")
                                and not str(line).__contains__("None")
                                and not str(line).__contains__("none")
                            ):
                                fp.write(str(line) + str("\n"))
                    print(f"Email password file for {fn} completed")

                if username in headers:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    comboUser = df[username] + ":" + df[password]
                    with open(
                        f"{dest_path.parent}\{stem}_username.txt", "w", encoding="utf_8"
                    ) as fp:
                        for line in comboUser:
                            if (
                                not str(line).__contains__("nan")
                                and not str(line).__contains__("<blank>")
                                and not str(line).__contains__("?")
                                and not str(line).__contains__("None")
                                and not str(line).__contains__("none")
                            ):
                                fp.write(str(line) + str("\n"))
                    print(f"Users password file for {fn} completed")

                if salt in headers:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    comboUser = df[username] + ":" + df[salt]
                    with open(
                        f"{dest_path.parent}\{stem}_salt.txt", "w", encoding="utf_8"
                    ) as fp:
                        for line in comboUser:
                            if (
                                not str(line).__contains__("nan")
                                and not str(line).__contains__("<blank>")
                                and not str(line).__contains__("?")
                                and not str(line).__contains__("None")
                                and not str(line).__contains__("none")
                                
                            ):
                                fp.write(str(line) + str("\n"))
                    print(f"Salt password file for {fn} completed")

                if phone in headers:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    comboUser = df[phone] + ":" + df[password]
                    with open(
                        f"{dest_path.parent}\{stem}_phone.txt", "w", encoding="utf_8"
                    ) as fp:
                        for line in comboUser:
                            if (
                                not str(line).__contains__("nan")
                                and not str(line).__contains__("<blank>")
                                and not str(line).__contains__("?")
                                and not str(line).__contains__("None")
                                and not str(line).__contains__("none")
                                and not str(line).__contains__("20%")
                            ):
                                fp.write(str(line) + str("\n"))
                    print(f"Phone password file for {fn} completed")
            except Exception as e:
                print(e)
                fix_path.parent.mkdir(parents=True, exist_ok=True)
                move_file(src_path.parent, fix_path.parent, fn)


