import csv
import os
import re
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def process_file(file_path):
    folder_path, file_name = os.path.split(file_path)
    if file_name.endswith('.txt'):
        input_file_path = file_path
        output_file_path = os.path.join(folder_path, file_name.replace('.txt', '.csv'))
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Timestamp', 'Length', 'Number'])
            for line in input_file:
                timestamp = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                length = re.search(r'length (\d+)', line)
                number = re.search(r"'(\d+\.\d+\.\d+\.\d+)', \d+, (\d+)", line)
                if timestamp and length and number:
                    writer.writerow([timestamp.group(), length.group(1), number.group(2)])

main_folder_path = 'data/baseline/baseline'
file_paths = []
for folder_path, subfolders, file_names in os.walk(main_folder_path):
    for file_name in file_names:
        file_paths.append(os.path.join(folder_path, file_name))

with ProcessPoolExecutor() as executor:
    list(tqdm(executor.map(process_file, file_paths), total=len(file_paths)))