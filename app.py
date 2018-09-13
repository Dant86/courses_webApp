import requests
import pandas as pd
from flask import Flask

# splitting up URL to comply with flake8 style standard
header = "https://docs.google.com/spreadsheets/d/"
spreadsheet_id = "1DHD8UPD7xFTp3WybTdrCKzDX_VjTQ_1gn1IIV5wysxA/"
ext = "export?gid=0&format=csv"

full_url = header + spreadsheet_id + ext

# reading the course data into a dataframe
df = pd.read_csv(full_url, index_col=0)

def is_valid_course(course):
    if pd.isnull(course):
        return False
    if "N/A" in course || "NA" course:
        return False
    if course == "nada":
        return False
    if course == "none":
        return False
    if ":" not in course:
        return False
    return True

def is_int(char):
    try:
        int(char)
        return True
    except:
        return False

def parse_time_from_course_name(name):
    # find the colon
    # go back until no longer a number
    # go forward until not a number
    ret = ":"
    index_colon = name.index(":")
    # There's a chance that the name
    # has a colon
    if not is_int(name[index_colon - 1]):
        index_colon += name[index_colon + 1:].index(":")
    cur_index = index_colon
    # backward pass
    while True:
        cur_index -= 1
        if not is_int(name[cur_index]):
            break
        ret = name[cur_index] + ret
    cur_index = index_colon
    # forward pass
    while True:
        cur_index += 1
        if cur_index == len(name):
            break
        if not is_int(name[cur_index]):
            break
        ret += name[cur_index]
    return ret

def index_of_first_num(string):
    counter = 0
    for char in string:
        if is_int(char):
            return counter
        counter += 1

def parse_humanities(name):
    name = name.replace(" T Th", "")
    if "Social Science Inquiry" in name:
        return "Social Science Inquiry"
    if "(" in name:
        return name[:name.index("(") - 1]
    else:
        return name[:index_of_first_num(name) - 1]

def parse_sosc(name):
    # same as humanities, so I'll just call
    # that function here
    return parse_humanities(name)

def parse_major(name):
    name = name.replace("H ", "Honors ")
    name = name.replace("Molec  ", "Molec ")
    name = name.replace("Mol ", "Molec ")
    name = name.replace("Comp Sci", "Computer Science")
    if "Honors Gen Chem" in name:
        return "Honors Chem"
    return parse_humanities(name)

def parse_math(name):
    name = name.replace("2", "II")
    if "H Calculus" in name or ("Honors Calculus" in name and "IBL" not in name):
        return "Honors Calculus I"
    parsed = parse_humanities(name)
    if parsed == "Calculus ":
        parsed = "Calculus I"
    if parsed == "Elem Functions + Calculus":
        return "Elem Functions + Calc"
    if parsed == "Calculus III MWF":
        return "Calculus III"
    return parsed

course_list = []
times = {
    "Humanities": {},
    "Sosc/Civ": {},
    "Major": {},
    "Math": {},
    "Science": {},
    "Elective": {}
}

'''
    I'm debugging this course-type by course-type,
    so I'm not iterating over anything yet, but
    the code will get significantly shorter once
    I'm done debugging.
'''
for i in range(len(df)):
    courses = df.iloc[i][:-2]
    hum = courses["Humanities Class"]
    if (is_valid_course(hum)):
        parsed_hum = parse_humanities(hum)
        time = parse_time_from_course_name(hum)
        if parsed_hum not in course_list:
            course_list.append(parsed_hum)
            times["Humanities"][parsed_hum] = [time]
        else:
            if time not in times["Humanities"][parsed_hum]:
                times["Humanities"][parsed_hum].append(time)
    sosc = courses["Sosc/Civ Class"]
    if (is_valid_course(sosc)):
        parsed_sosc = parse_humanities(sosc)
        time = parse_time_from_course_name(sosc)
        if parsed_sosc not in course_list:
            course_list.append(parsed_sosc)
            times["Sosc/Civ"][parsed_sosc] = [time]
        else:
            if time not in times["Sosc/Civ"][parsed_sosc]:
                times["Sosc/Civ"][parsed_sosc].append(time)
    major = courses["Major Class"]
    if (is_valid_course(major)):
        parsed_major = parse_major(major)
        time = parse_time_from_course_name(major)
        if parsed_major not in course_list:
            course_list.append(parsed_major)
            times["Major"][parsed_major] = [time]
        else:
            if time not in times["Major"][parsed_major]:
                times["Major"][parsed_major].append(time)
    math = courses["Math Class"]
    if (is_valid_course(math)):
        parsed_math = parse_math(math)
        time = parse_time_from_course_name(math)
        if parsed_math not in course_list:
            course_list.append(parsed_math)
            times["Math"][parsed_math] = [time]

print(times["Math"])



