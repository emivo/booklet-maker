#!/usr/bin/python3
import os
import re
def main():
    print("###################################")
    print("#                                 #")
    print("#         Bookletpro 2000         #")
    print("#                                 #")
    print("###################################")
    print("This script removes the timestamps, IF THEY ARE IN CORRECT PLACE, from the abstracts in Abstracts_(invited|short)") 

    print("Processing abstracts...\n")
    process_files("Abstracts_short")
    process_files("Abstracts_invited")

def process_files(directory):
    print(f"Processing directory: {directory}")
    for file in sorted(os.listdir(directory)):
        if file.endswith('.tex'):
            file_path = os.path.join(directory, file)
            match = re.search(r'([^\\/]+)_(.*)\.tex$', file)
            if match:
                key = match.group(2)
                print(f"Processing file: {file_path}, extracted key: {key}")
                remove_time_from_file(file_path)
    print(f"All good in {directory}")



def remove_time_from_file(file_path):
    output_lines = []
    line_after_name = False
    time_removed = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "\\normalsize" in line:
            line_after_name = True
            output_lines.append(line)
            print("Row with \\normalsize found") # Debugging, remove later
            continue

        if line_after_name and not time_removed:
            if re.search(r'(|\d)\d.\d\d +?-- +?(|\d)\d.\d\d',line):
                time_removed = True
                print(f"The line after the \\normalsize have been removed")
                continue 
        output_lines.append(line)
    if  line_after_name and not time_removed:
        print("Timestamp not found") #Debug
        return 

    with open(file_path, 'w') as file:
        file.writelines(output_lines)

if __name__ == "__main__":
    main()



