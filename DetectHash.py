import hashlib
import os

hash_algorithms = {
    32: 'MD5',
    40: 'SHA1',
    64: 'SHA2',
    128: 'SHA512',
    32: 'MD5 Wordpress',
    32: 'MD5 phpBB',
    60: 'BCRYPT',
    34: 'MD5-Crypt',
    34: 'PHPass',
    64: 'PBKDF2-SHA256',
    64: 'NTLMV1',
    128: 'NTLMV2',
    60: 'Blowfish',
    64: 'Twofish',
    128: 'ThreeFish',
    32: 'AES-128',
    48: 'AES-192',
    64: 'AES-256'
}


def get_hash_type(hash_str):
    hash_len = len(hash_str)
    if hash_len in hash_algorithms:
        return hash_algorithms[hash_len]
    else:
        # Hash length doesn't match any known algorithm
        return 'Unknown'

# Set input folder name
input_foldername = r'/path'

# Traverse folder structure and process each text file
for root, dirs, files in os.walk(input_foldername):
    for file in files:
        if file.endswith('.txt'):
            # Set input and output file paths
            input_filepath = os.path.join(root, file)
            output_filename = os.path.splitext(file)[0] + '_hash_types.txt'
            output_foldername = root

            try:
                # Determine hash algorithm types for all hash strings in input file
                with open(input_filepath, encoding='utf-8') as f:
                    hash_strings = [line.strip() for line in f if line.strip()]

                hash_types = set(get_hash_type(hash_str.split(":")[1]) for hash_str in hash_strings)

                # Construct output file name based on detected hash algorithm types
                if len(hash_types) == 1:
                    output_filename = os.path.splitext(file)[0] + f"_{list(hash_types)[0]}.txt"
                else:
                    output_filename = os.path.splitext(file)[0] + '_multi'
                    for hash_type in hash_types:
                        output_filename += f"_{hash_type}"
                    output_filename += '.txt'

                output_filepath = os.path.join(output_foldername, output_filename)

                # Write hash algorithm types for each hash string to output file
                with open(output_filepath, 'w') as f:
                    for hash_str in hash_strings:
                        try:
                            parts = hash_str.split(":")
                            hash_value = parts[1].strip()
                            hash_type = get_hash_type(hash_value)
                            f.write(f"{hash_str}:{hash_type}\n")
                        except IndexError:
                            # Invalid hash string format, skip this line
                            pass

                # Rename input file to output file
                os.remove(input_filepath)
                # os.rename(output_filepath, input_filepath)

            except FileNotFoundError:
                print(f"File not found: {input_filepath}")
            except IndexError:
                print(f"IndexError processing file: {input_filepath}")
