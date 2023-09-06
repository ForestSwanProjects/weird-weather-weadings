"""
Extract raw weather readings data
_________________________
Notes:
- Using record class isn't really necessary until we want to extract all info from each line and use multiple lines.

"""

import re
import json
import datetime as dt

#function to get next line boundaries
def get_next_line(line, data):

    next_start = len(line)+1
    next_end = data.find("\n", next_start)

    new_line = data[next_start:next_end]

    return new_line


#function to check line format
def check_line_format(line_to_test):

    #the start of none of the invalid records match this format
    template = re.compile("^[0-3][0-9][/][0-1][0-9][/][2][0][2][3]\s[0-2][0-9][:][0-5][0-9][:][0-5][0-9][,][0][R][0][,][D][n]")
    
    if template.match(line_to_test):
        return True
    else:
        return False
    

#function to find the next invalid record
def find_next_bad_record(file, line):
    
    #while line fits format, go to next line
    while check_line_format(line):

        previous = line

        line = file.readline()

    return previous, line


#function to find the next valid record
def find_next_good_record(file, line):

    #while line does not fit format, go to next line
    while not check_line_format(line):

        line = file.readline()

    return line


### START

with open("file_paths.json") as paths:
    paths_dict = json.load(paths)

data_file = paths_dict["raw_data"]

f = open(data_file, "r", encoding='ANSI')
line = f.readline()

#for colum numbers from below line, -2
#01/07/2023 00:00:03,0R0,Dn=095D,Dm=274D,Dx=352D,Sn=0.3M,Sm=5.8M,Sx=9.6M,Ta=17.9C,Ua=73.7P,Pa=1.0058B,Rc=13.02M,Rd=12480s,Ri=0.0M,Hc=0.0M,Hd=0s,Hi=0.0M,Th=18.0C,Vh=12.1N,Vs=12.1V,Vr=3.631V

"""
COULD CREATE A RECORD CLASS WITH BELOW AS ATTRIBUTES? - see above notes
   https://docs.python.org/3/tutorial/classes.html
   https://www.w3schools.com/python/python_classes.asp

date = line[0:10]
time = line[11:19]

#find e.g. "Rc" in string, get value between "=" and ","
rain_accum = line[line.find("Rc")+3:line.find(",",line.find("Rc"))-1]
rain_dur = line[line.find("Rd")+3:line.find(",",line.find("Rd"))-1]
rain_inten = line[line.find("Ri")+3:line.find(",",line.find("Ri"))-1]
air_temp = line[line.find("Ta")+3:line.find(",",line.find("Ta"))-1]
supply_V = line[line.find("Vs")+3:line.find(",",line.find("Vs"))-1]
ref_V = line[line.find("Vr")+3:line.find(",",line.find("Vr"))-1]
"""

#list of dates/times of lines where problems start or are found
problem_lines = []

#while next line is not end of file
while next_line != "":

    #write new get next line funtion
    #next_line = get_next_line()

    prev_line, invalid_line = find_next_bad_record(f, line)

    invalid_line_dt = invalid_line[0:19]
    invalid_line_dt = dt.datetime.strptime(invalid_line_dt, "%d/%m/%Y %H:%M:%S")

    prev_line_dt = prev_line[0:19]
    prev_line_dt = dt.datetime.strptime(prev_line_dt, "%d/%m/%Y %H:%M:%S")

    next_valid_line = find_next_good_record(f, invalid_line)

    next_dt = next_valid_line[0:19]
    next_dt = dt.datetime.strptime(next_dt, "%d/%m/%Y %H:%M:%S")

    #if previous record to invalid_line is within half an hour(THIS CAN CHANGE),
    # get records from previous 2 hours every 5 minutes(THESE CAN ALSO CHANGE) up to last valid record,
    # use these records to chart rainfall
    time_diff = invalid_line_dt - prev_line_dt

    if (time_diff.seconds / 60) < 30:

        record_found = False

        search_date = invalid_line_dt - dt.timedelta(hours=2)

        print(str(search_date))

        while record_found != True:

            curr_line = f.readline()

            #if date of line 2 hours prior, line found

    else:
        print(invalid_line_dt)
        print(prev_line_dt)
        print(time_diff)



    #if following record to next_valid_line is within 5 mins,
    # get records for next 2 hours every 5 mins,
    # chart rainfall

    #chart scraped data to compare and fill in the gaps

f.close()
