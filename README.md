# Conference Booklet/Program Template

This repository contains a template for generating a booklet or program for a conference. Follow the instructions below to prepare and compile your conference booklet.

## Abstract Preparation

1. **Save Abstracts**: Store abstracts in folders named `Abstracts_*`. These abstracts will be automatically included in the booklet.
2. **File Naming**: Use the filename format `conference_lastname.tex`. This ensures that abstracts are sorted alphabetically by the last name.
3. **Template Usage**: Follow the template in the provided folders. Extracting names and titles relies on `\Large` for names and `\huge` for titles. Ensure names and titles are on their respective lines.
4. **Compilation**: Use the standalone class to compile and view abstracts individually. This makes them easy to integrate into the program.
5. **Commands**: Do not include new commands in the subfiles. Keep the `\normalsize` command in the center section, as it indicates where to place timestamps.

## Timestamps and Timetables

- **Manual Timetable Creation**: The template does not automate timetable creation or talk allocation due to various influencing factors. This requires manual input.
- **Time Insertion**: If tables follow the template format, the script will insert times into the abstract files. For normal talks, the time is taken from the left-most column and the day from the top row. For parallel talks, the date should be in the center section.
- **Update Mechanism**: The script updates any changes to the times. If issues arise, use the provided script to remove timestamps.

## CSV File for Certificates

The script generates a CSV file listing speakers and titles, which can be used to create certificates.

1. **Certificates**: Use `process_csv_certificates.py` to generate certificates.
2. **Template Customization**: Customize your certificate template. The provided template is for demonstration purposes.
3. **Command**: Run `python3 process_csv_certificates.py (participation || talk)` to create certificates. The script can handle both participation and talk certificates with `input_participation.csv`.

## Modifying the Template

- **Placeholder Addition**: Add placeholders for new speakers using `{Talk \d}` for normal talks and `{STalk \d}` for parallel talks.
- **Schedule Geometry**: Adjust the main schedule manually as the current geometry is basic.

## Requirements

- Python 3
- pdflatex
- latexmk

### Tested on Ubuntu 22.04

## Future Improvements

- Script for automatic timetable creation
- User prompts for:
  - Certificate creation
  - Talk allocation
- Optimization: Reduce rewrites and improve runtime efficiency using tools like [TexSoup](https://github.com/alvinwan/TexSoup)

&copy; Emil Airta 2024

Improvements and suggestions are welcome.
