import csv
from googletrans import Translator
import os

# Set the input CSV file, target language, and output CSV file
input_file = 'input.csv'
target_language = 'en'
output_file = 'output.csv'

# Initialize the translator
translator = Translator()

# Open the input CSV file and read the headers
with open(input_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames

# Translate the headers to English
translated_headers = []
for header in headers:
    translated = translator.translate(header, dest=target_language)
    translated_headers.append(translated.text)

# Replace the original headers with the translated headers
with open(input_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    with open(output_file, 'w', newline='', encoding='utf-8') as g:
        writer = csv.DictWriter(g, fieldnames=translated_headers)
        writer.writeheader()
        for row in reader:
            writer.writerow(row)

# Rename the output CSV file to the input CSV file
os.rename(output_file, input_file)
