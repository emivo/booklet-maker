#!/bin/python3
#Author: Emil Airta
# Import necessary libraries
import os
import re
# Function to get user input for the schedule
def get_schedule():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    time_slots = []
    time_slots_with_same_activity = {} 
    schedule = {day: {} for day in days}
    parallel_days = []
    talk  = 0 #Running number of normal talks
    stalk = 0 #Running number of parallel sessions
    #TODO: ADD default setup
   
    print("Enter number of days (e.g. for Mon-Fri enter 5) or use default:")
    num_days = input()
    try:
        num_days = int(num_days)
    except ValueError:
        def_time_slots = [f"{a}.00 -- {a + 1}.00" for a in range(9,16)]
        def_parallel_days = ["Tuesday","Thursday"]
        def_parallel = {ses + 1: {'15.00 -- 15.30': ["{Stalk 1}","{Stalk 2}"]} for ses in range(len(def_parallel_days))} 
        def_schedule = {day: {} for day in days[:5]} 
        for time in def_time_slots:
            for day in days[:5]:
                activity = "{Talk 1}"
                def_schedule[day][time] = activity
        for par_day in def_parallel_days:
            def_schedule[par_day]['15.00 -- 16.00'] = "Short talks"
        return def_time_slots,def_schedule,def_parallel,def_parallel_days
    print(f"Enter start day (options: {days[:8-num_days]}): ")
    start_day = input()
    ind_start_day = days.index(start_day)
    days = days[ind_start_day:num_days]
    print("Enter the time slots for the schedule (e.g., 9-10 AM or 9.00 -- 10.00). Press enter when done.")
    while True:
        time_slot = input("Enter time slot (or press enter to finish): ")
        if not time_slot:
            break
        time_slots.append(time_slot)
    
    for day in days:
        #add option of population each time_slot with the same
        print(f"Enter the schedule for {day}:")
        for time_slot in time_slots:
            #Check if we already wantend something on that activity
            if time_slot in time_slots_with_same_activity.keys():
                activity = time_slots_with_same_activity[time_slot]
                if "short" in activity:
                    stalk += 1
                    activity = f"\\hyperlink{{short{stalk}}}{{Parallel session {stalk}}}\\hypertarget{{bS{stalk}}}{{}}"
                    parallel_days.append(day)
                elif "talk" in activity:
                    talk += 1
                    activity = f"{{Talk {talk}}}"
                schedule[day][time_slot] = activity
                continue
            #Else we ask for new
            print(f"Enter activity for {time_slot}: Entering 'talk' will give placeholder for talks and 'short' is placeholder for parallel session")
            activity = input()
            every_day = input("Do you want this activity for all the rest of the days (y,n)? \t ")
            if every_day.lower() in ['y','yes']:
                time_slots_with_same_activity[time_slot] = activity
            if "short" in activity:
                stalk += 1
                activity = f"\\hyperlink{{short{stalk}}}{{Parallel session {stalk}}}\\hypertarget{{bS{stalk}}}{{}}"
                parallel_days.append(day)
            elif "talk" in activity:
                talk += 1
                activity = f"{{Talk {talk}}}"
            schedule[day][time_slot] = activity
    if stalk > 0:
        parallel = get_parallel(stalk)
    return time_slots, schedule, parallel, parallel_days
# Function to make parallel schedule, returns the rooms as number of rooms per session and dictionary schedule with the {Stalk \d} placeholder for each time slot
def get_parallel(number_of_sessions):
    schedule = {session + 1: {} for session in range(number_of_sessions)}
    talk_number = 0 #Running talk number. This is actually unnessasary and could be calculated from session + rooms[session]
    
    for session in range(number_of_sessions):
        session_tmp = session + 1
        print(f"Enter the number of parallel talks in session {session_tmp}:")
        num = int(input())
        print("Enter the time slots for the schedule (e.g., 9-10 AM or 9.00 -- 10.00). Press enter when done.")
        while True:
                time_slot = input("Enter time slot (or press enter to finish): ")
                if not time_slot:
                    break
                schedule[session_tmp][time_slot] = [f"{{Stalk {a + 1 + talk_number}}}" for a in range(num)]
                talk_number += num
    return schedule

# Function to generate LaTeX code for the schedule
def generate_latex_schedule(time_slots, main_schedule,par_schedule,par_days):
    # Check if we already have a template
    if os.path.isfile("booklet.tex"):
        #remove this when finished or add to main
        print("Do you want to use the existing template? (Yes,No)")
        answer = input()
        if answer.lower() in ['y','yes']:
            # Read the template file and insert in place holders
            with open("booklet.tex",'r', encoding='utf-8') as file:
                latex_code = file.read()
                return replace_timetables(time_slots,main_schedule,par_schedule,par_days,latex_code)
        else:
            return template_maker(time_slots,schedule)
    else:
        return template_maker(time_slots, schedule)

def replace_timetables(time_slots,main,parallel,par_days,latex_code):
    # find BEGIN{MAIN}
    regex_pattern = r"%-- BEGIN{MAIN}(.|\n|\r)*?%-- END{MAIN}"
    # Replace between END{MAIN}: 
    hack_str_escapes_in_latex_code = table_content_maker(time_slots,main,"main".upper()).replace("\\","\\\\")
    new_latex_code, num_replacements = re.subn(regex_pattern, rf"{hack_str_escapes_in_latex_code}", latex_code, count=1)
    if num_replacements == 0:
        print(f"No markers found for replacement")
        #TODO error handeling in this case
    else:
        latex_code = new_latex_code
    
    #find BEGIN{STABLES}
    
    replacement = make_stables(parallel, par_days).replace("\\","\\\\")
    regex_pattern = r"%-- BEGIN{STABLES}(.|\n|\r)*?%-- END{STABLES}"
    new_latex_code, num_replacements = re.subn(regex_pattern,replacement,latex_code,count=1)
    if num_replacements == 0:
        print(f"No markers found for replacement")
        #TODO error handeling in this case
    else:
        latex_code = new_latex_code
    
    return latex_code
def make_stables(parallel,days):
    stables = ""
    for session in parallel.keys():
        #add header
        rooms = len(parallel[session])

        header= make_tabular_header(rooms,session,days[session -1],"STABLES")
        #new markers
        marker = f"stable{session}"
        table_conten = table_content_maker(parallel[session].keys(),parallel,marker.upper())
        #add end of table
        end = make_tabular_end("STABLES")
        #Append to the return variable stables
        stables += header + table_conten + end
    return stables


def table_content_maker(time_slots, schedule,latex_markers_for_content): 
    selected_days = schedule.keys()
    code = f"%-- BEGIN{{{latex_markers_for_content}}}\r"
    #Hack to make main schedule header TODO make uniform for all
    if len(selected_days) > 0 and type(list(selected_days)[0]) is str:
        code += "\\begin{tabularx}{1.3\linewidth}{| c |"
        code += " X |" * len(selected_days)
        column_headers = " TIME & "
        column_headers += " & ".join(list(selected_days)) #TODO: textbf
        code += "}\n" + column_headers + "\n"
    for time_slot in time_slots:
        code += f"{time_slot} & "
        for day in schedule.keys():
            #day is actually room if parallel session, consider renaming to col
            activity = schedule[day].get(time_slot, " ")
            if type(activity) is list:
                for talk in activity:
                    code += f"{talk} & "
            else :
                code += f"{activity} & "
        code = code[:-2] + " \\\\ \n\\hline\n" #first part will strip the last align character
    code += "\\end{tabularx}"
    code += f"%-- END{{{latex_markers_for_content}}}"
    return code 
# DO NOT REMEMBER WHY THIS FUNCTION IS HERE
def add_parallel_tables(parallel,schedule):
    #Find the days

    #Make a table for that day

    # Separate the contents
    #return
    pass
def make_tabular_header(num_col,session_number,day,marker):
    code = f"%-- BEGIN{{{marker}}}\n"
    code += r"""\begin{center}"""
    code += f"\\hypertarget{{short{session_number}}}{{\\textsc{{\\Large\\hyperlink{{bS{session_number}}}{{{day}}}}}}}"
    code += r""" 
		\end{center}
        """
    code +=  r"""
	\begin{table}[htbp]
		\centering
		\begin{tabularx}{\textwidth}{c| """
    for i in range(num_col):
        code += " X |"
        code += """}
			\hline
            """
    for i in range(num_col):
        code += f"& \\textbf{{Room {i + 1}}}"
        code += r"""\\ \hline"""
    return code
def make_tabular_end(marker):
    code =  r"""
    		\end{tabularx}
		\end{table}
        """
    code += f"\n%-- END{{{marker}}}\n"
    return code  
### TODO: THIS IS NOT WORKING YET
def template_maker(time_slots, schedule):
    #TODO: modify the weekschedule to coincide with the schedule.keys() lenght
    #Also TODO: parallel maker not workin
    column_spec = "l|" + "X|" * len(selected_days)
    column_headers = " & ".join(selected_days)
    latex_code = r"""
%%% AUTHOR: Emil Airta
%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------
\documentclass{article}
\usepackage{tabularx}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\begin{document}
%----------------------------------------------------------------------------------------
%	SCHEDULE GENERAL
%----------------------------------------------------------------------------------------
\section*{Schedule}
\begin{tabularx}{\textwidth}{|l|X|X|X|X|X|X|X|}
\hline
Time & Monday & Tuesday & Wednesday & Thursday & Friday & Saturday & Sunday \\
\hline
"""
    #Add main schedule
    latex_code += table_content_maker(time_slots,schedule) 
    #Add parallel schedules
    latex_code += r"""
\end{tabularx}
\pagebreak
%----------------------------------------------------------------------------------------
%	SCHEDULE PARALLEL
%----------------------------------------------------------------------------------------
\begin{center}
\textsc{\LARGE Short talks schedule}
\end{center}
"""
    latex_code += make_stables(parallel,latex_code) #CHECK WHAT IS HAPPENING TODO
#    for session in parallel.keys()
#        latex_code += make_tabular_header(len(par_schedule.keys()),) 
#        latex_code += add_parallel_tables(time_slots_short,parallel,days)
#        latex_code += make_tabular_end() 
    latex_code += r"""

%% --------------------------------------------------------------------
%              BEGINING OF INVITED
%% -------------------------------------------------------------------
\section{Invited talks}
\input{inputs_invited}
%% --------------------------------------------------------------------
%              END OF INVITED
%% -------------------------------------------------------------------
\pagebreak
%% --------------------------------------------------------------------
%              BEGINING OF SHORT
%% -------------------------------------------------------------------
\section{Short talks}
\input{inputs_shorts}

%% --------------------------------------------------------------------
%              END OF SHORT
%% -------------------------------------------------------------------
\end{document}
"""
    return latex_code

# Main function to run the script
def main():
    time_slots, main_schedule, par_schedule, par_days = get_schedule()
    latex_code = generate_latex_schedule(time_slots, main_schedule,par_schedule, par_days)
    
    #TODO: change here booklet.tex
    file_path = "weekly_schedule.tex"
    with open(file_path, "w") as f:
        f.write(latex_code)
    
    print(f"LaTeX code for the schedule has been generated and saved to {file_path}.")
    
    #flags? TODO
    print("Do you already have some abstracts to add?")
    ans = input()
#    if ans.lower() in ["y","yes"]:
        # updatescript1 TODO

if __name__ == "__main__":
    main()

