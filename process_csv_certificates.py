#!/usr/bin/python3
#Author Emil Airta
import csv
import sys
import os
import subprocess

def generate_file(template, user, title, typedoc):
    """
    Generate a LaTeX file and compile it to PDF for a given user.

    Parameters:
    - template: The LaTeX template as a string.
    - user: The name of the speaker.
    - title: The title of the user's talk (optional).
    - typedoc: The type of document (e.g., 'talk' or 'participation').
    """
    # Construct the path for the user's output directory
    path_to = os.path.join(typedoc, user.replace(' ', '_'))
    os.makedirs(path_to, exist_ok=True)

    userfilename = user.replace(' ', '_')
    temp = os.path.join(path_to, f'certificate_{userfilename}_{typedoc}')
    filename = f'{temp}.tex'
    
    # Create LaTeX file with user data
    with open(filename, 'w', encoding='utf-8') as latex_file:
        latex = template.replace(r'{user}', user)
        if title is not None:
            latex = latex.replace(r'{title}', title)
        latex_file.write(latex)

    print(f'Generated LaTeX file: {filename}')
    
    # Compile LaTeX to PDF using latexmk
    print(f'Compiling {filename} to PDF...')
    result = subprocess.run(
        ['latexmk', '-pdf', '-jobname=' + temp, filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if result.returncode != 0:
        print(f'Error compiling {filename}:\n{result.stderr}')
    else:
        print(f'Successfully compiled {filename} to PDF\n')

def main():
    # Check if the script is called with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <type>")
        print("<type> should be either 'talk' or 'participation'")
        sys.exit(1)

    typedoc = sys.argv[1]
    
    # Read LaTeX template file
    template_filename = f'certificate_temp_{typedoc}.tex'
    try:
        with open(template_filename, 'r', encoding='utf-8') as template_file:
            template = template_file.read()
        print(f'Read template file: {template_filename}')
    except FileNotFoundError:
        print(f"Template file '{template_filename}' not found.")
        sys.exit(1)
    
    # Read CSV input file
    csv_filename = f'input_{typedoc}.csv'
    try:
        with open(csv_filename, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                else:
                    if len(row) == 2:
                        # Generate file with user and title
                        generate_file(template, row[1], row[0], typedoc)
                    else:
                        # Generate file with only user
                        generate_file(template, row[0], None, typedoc)
                line_count += 1
            print(f'Processed {line_count - 1} lines.')
    except FileNotFoundError:
        print(f"CSV input file '{csv_filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()

