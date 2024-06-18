#!/usr/bin/python3
# Author: Emil Airta
# MIT Licence 
# 2024
import os
import re
import subprocess
from lib import LaTexAccents as tex


def process_files(directory, output_file, output_file_csv):
    print(f"Processing directory: {directory}")
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in sorted(os.listdir(directory)):
            if file.endswith('.tex'):
                file_path = os.path.join(directory, file)
                acronym = file.split("_")[0]
                speaker,title = extract_name_and_title(file_path, output_file_csv)
                match = re.search(r'([^\\/]+)_(.*)\.tex$', file)
                if match:
                    key = match.group(2)
                    print(f"Processing file: {file_path}, extracted key: {key}")
                    outfile.write("\\filbreak \n")
                    outfile.write(f"\\hypertarget{{{key}}}{{\\input{{{file_path}}}}}\n")
                    hyperkey = f"\\hyperlink{{{key}}}{{{speaker}}}"
                    replace_talks_in_file("booklet.tex", hyperkey,key, directory, acronym)
    print(f"Output written to: {output_file}\n")

def replace_talks_in_file(filename, hyperkey,key, directory, acronym):
    try:
        # Read the latex_code of the file
        with open(filename, 'r', encoding='utf-8') as file:
            latex_code = file.read()

        # Define the regex pattern to find {Talk <number>
        placeholder_type = 'STalk' if 'short' in directory else 'Talk'
        pattern = rf'{{{placeholder_type} (.+?)}}'
        # Check if the replacement has already been made
        target = re.search(r'(.+?})({.+?})',hyperkey)
        if target.group(1) in latex_code:
            print(f'The replacement "{hyperkey}" is already present in {filename}.')
            if 'short' in directory:
                day,time = extract_time_from_latex_short(latex_code,key)
                if day and time:
                    insert_time_into_file(directory, acronym, day + ' ' +  time, key)
                else:
                    print("There is some issue in extracting time and date from the table")
            else: 
                day, time = extract_time_from_latex_invited(latex_code,hyperkey,key)
                if day and time:
                    insert_time_into_file(directory, acronym, day + ' ' + time, key)
                else:
                    print("There is some issue in extracting time and date from the table")
            return

        # Replace the first occurrence of the placeholder with the replacement string

        new_latex_code, num_replacements = re.subn(pattern, "\\"+ hyperkey, latex_code, count=1)
        if num_replacements == 0:
            print(f"No placeholder Talk found in {filename}.")
        else:
            # Write the modified latex_code back to the file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(new_latex_code)
            print(f'Successfully replaced {placeholder_type} with "{hyperkey}" in {filename}.')
            # Add that time into the abstract
            print('Extracting time and day to put into the abstract files') #One could consider making more elegant solution so we do not need to mess with the abstract files..
            # One way could be that these are done in inputs_*.tex and we would have titles and abstracts separately
            if 'short' in directory:
                day,time = extract_time_from_latex_short(latex_code,key)
                if day and time:
                    insert_time_into_file(directory, acronym,day + ' ' +  time, key)
                else:
                    print("There is some issue in extracting time and date from the table")
            else: 
                day, time = extract_time_from_latex_invited(latex_code,hyperkey,key)
                if day and time:
                    insert_time_into_file(directory,acronym, day + ' ' + time, key)
                else:
                    print("There is some issue in extracting time and date from the table")
    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
# these are kind of working and I will make cleaning routine in case we need one
def insert_time_into_file(directory,acronym, time, key):
    input_file_path = os.path.join(directory, f"{acronym}_{key}.tex")
    output_lines = []
    line_after_name = False
    time_inserted = False

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "\\normalsize" in line:
            line_after_name = True
            output_lines.append(line)
            continue

        if line_after_name and not time_inserted:
            if time in line:
                print(f"Time '{time}' is already present after in {key}.tex")
                return
            else:
                placehold = 'short1' if 'short' in directory else 'talks'
                output_lines.append(f"\\hyperlink{{{placehold}}}{{{time}}}\n")
                time_inserted = True
                if re.search(r'\d\d.\d\d -- \d\d.\d\d',line): 
                    print("Updating previous time")
                    print(f"We will remove old time {line}") #Debug purpose
                    continue
        output_lines.append(line)
    if line_after_name == False and time_inserted == False:
        print("The name row not found") #Debug
        return 

    with open(input_file_path, 'w') as file:
        file.writelines(output_lines)

    print(f"Time '{time}' has been inserted into {key}.tex after the \\normalsize line.")
def extract_time_from_latex_invited(latex_code,hyperkey,key):
    day_tabular_pattern = re.compile(
    r'\\begin\{tabularx\}\{.+?\}\{.+?\}(.+?)\\end\{tabularx\}',
        re.DOTALL
    )
    day_time_pairs = day_tabular_pattern.findall(latex_code)
    for tabular in day_time_pairs:
        rows = tabular.split('\\\\')
        days_row = rows[0]
        for row in rows:
            match = re.search(rf'\\hyperlink{{{key}}}{{.+?}}', row)
            if match:
                row_split = [x.strip() for x in row.split('&')]
                time_value = row_split[0].strip()
                if '\n' in time_value:
                    time_value = time_value.split('\n')[1]
                days = days_row.split('&')
                inx = row_split.index(hyperkey)
                day = days[inx]
                return day.strip(), time_value.strip()

    return None, None

def extract_time_from_latex_short(latex_code, key):

    # Regular expression to match rows and capture the time and key
    day_tabular_pattern = re.compile(
        r'\\begin{center}.*?\\textsc{\\Large\\hyperlink{.*?}{(.*?)}.*?\\end{center}.*?\\begin{tabularx}{.*?}(.*?)\\end{tabularx}',
        re.DOTALL
    )
    day_time_pairs = day_tabular_pattern.findall(latex_code)

    for day, tabular in day_time_pairs:
        rows = tabular.split('\\\\')
        for row in rows:
            match = re.search(rf'\\hyperlink{{{key}}}{{.+?}}', row) #notice that we should only work with the hyperkey not the key
            if match:
                time_value = row.split('&')[0].strip()
                if '\n' in time_value:
                    time_value = time_value.split('\n')[1]
                return day.strip(), time_value
    return None, None

def extract_name_and_title(input_file, output_file):
    print("Extracting author name and title")
    print(f'Accessing file: {input_file}')
    with open(input_file, 'r') as infile:
        #add the header
        csv_collector = ""
        rname,rtitle = "",""
        for line in infile:
            name = extract_pattern(line, r'Large (.+?)( |)(\\)(\\)')
            if name:
                name = name.strip()
                name = tex.AccentConverter().decode_Tex_Accents(name,utf8_or_ascii=1)
                csv_collector += name + '\n'
                rname = name
            title = extract_pattern(line, r'huge (.+?)( |)(\\)(\\)')
            if title:
                csv_collector += title + ','
                rtitle = title
        print(f"Found: {rname} is giving a talk entitled {rtitle}")
        append_to_file(output_file, csv_collector)
        return rname,rtitle
#following two functions do not make sense... these were initially for documentation and debuging purposes
def init_pattern(pattern):
    return pattern + '(.+?)\%'
def extract_pattern(line, pattern):
    # One could change the template of the abstracts such that we could find name and the title between some comments
    # e.q.
    # \huge
    # % TITLE
    #
    # % --
    # % AUTHOR
    #
    # % --
    # Then we could grab these whole lines between the markers. Of course there is going to be issues because
    # users might not follow what we want
    target = re.search(pattern, line)
    if target:
        return target.group(1)
    return None

def append_to_file(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text)

def main():
    print("###################################")
    print("#                                 #")
    print("#         Program automation      #")
    print("#                                 #")
    print("###################################")
    print(" Author (c) Emil Airta, version 1.0, 2024")
    print("This is a simple script to make a LaTeX booklet of given files. Please see the README for the instructions for setting up the files.\n")
    
    print("initialize csv for certificates")
    output_file_csv = "input_talk.csv"
    open(output_file_csv, 'w').close()
    append_to_file(output_file_csv,'TITLE,USER\n')

    print("Processing abstracts...\n")
    process_files("Abstracts_short", "inputs_shorts.tex", output_file_csv)
    process_files("Abstracts_invited", "inputs_invited.tex", output_file_csv)

    print("Initiating latexmk with pdflatex and minimal output...\n")
    result = subprocess.run(
        ["latexmk", "-pdf", "-pdflatex=pdflatex -file-line-error -interaction=nonstopmode", "booklet.tex"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    output = result.stdout
    errors = result.stderr

    if output:
        print("LaTeXmk Output:")
        for line in output.split('\n'):
            if re.match(r'^.*:[0-9]*: .*$', line):
                print(line)

    if errors:
        print("\nLaTeXmk Errors:")
        print(errors)

    print("\nLaTeX compilation finished.\n")

if __name__ == "__main__":
    main()

