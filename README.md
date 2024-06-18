# This is the template for making a booklet/program for a conference
Save abstracts to folders Abstracts\_\* and these will be automatically added to the booklet.
You should use the filename `conference_lastname.tex` so that everything works correctly, and abstracts are ordered alphabetically using the last name.
Also, please use the template demonstrated in these folders since names and titles are extracted using the \Large and \huge as indicators of each line. So, one should keep the name and title in the same line.
Moreover, the standalone class is neat so people can compile and view their abstracts and then these are easy to input into the program. Note that any newcommands are not inputted from the subfiles.
`\normalsize` command should be kept in the center section as this is an indicator for placing the timestamps.

This template does not provide yet any method of automatically making the timetables and allocating the given talks as this will be affected by so many factors and will need human assistance.
However, the script will place the times into the abstract files if the tables are like in the template file. That is, for normal talks, it will take the time from the left-most column
and the day of the week is extracted from the top row. For the parallel talks, the date should be in the center section according to the current format.
The script updates any changes to the times, but if it is not working there is a script to remove timestamps.

The script will also make separate a CSV file for speakers and titles of the talks so one can make use of the process script to make certificates using the chosen template they have.
This script will change {title} and {user} from the given file and compile these files using pdflatex. You have to make your template and the one here is only for demonstration purposes.
You should call `python3 process_csv_certificates.py (participation || talk)` since there is also an option of making certificates for participation with input\_participation.csv.


If you modify the tables and add more placeholders for speakers, write {Talk \d} for a normal talk with any number in place of \d and for parallel talks {STalk \d}. This way new abstracts can be placed there.

Notice that the main schedule contains geometry that is not to most brilliant since one needs to make adjustments by hand
## Requirements
- python3
- pdflatex
- latexmk

----
## What would be nice
- script to make tables
- user prompt:
	- make the certificates
	- allocations of the talks
- optimization: currently, almost everything is rewritten and only latexmk is helping with runtime. 


&copy; Emil Airta 2024
Improvements and suggestions are welcome.


 
