#extract raw weather readings data

import re
import json

#function to get next line boundaries - THIS DOES NOT WORK
def get_next_line(curr_end, data):

    start = curr_end + 1

    date_pattern = re.compile("[0-3][0-9][/][0-1][0-9][/][2][0][2][3]")

    end = re.search(date_pattern, data).start()
    print(end)
    return start, end

#function to check line format
def check_line_format(line_to_test):

    #the start of none of the invalid records match this format
    template = re.compile("^[0-3][0-9][/][0-1][0-9][/][2][0][2][3]\s[0-2][0-9][:][0-5][0-9][:][0-5][0-9][,][0][R][0][,][D][n]")
    
    if template.match(line_to_test):
        return True
    else:
        return False
    
#function to find the next invalid record
def find_next_bad_record(data, line):
    
    #while line fits format, go to next line
    while check_line_format(line):

        date = line[0:10]
        time = line[11:19]

        line_start, line_end = get_next_line(len(line)-1, data)
        line = data[line_start:line_end]

    #print("date + time of last valid line:",date,time)

    return line

#function to find the next valid record
def find_next_good_record(data, line):

    date = line[0:10]
    time = line[11:19]

    while not check_line_format(line):

        date = line[0:10]
        time = line[11:19]

        line_start, line_end = get_next_line(len(line)-1, data)
        line = data[line_start:line_end]

    #print("date + time of last invalid line:",date,time)

    return line

### START

with open("file_paths.json") as paths:
    paths_dict = json.load(paths)

data_file = paths_dict["raw_data"]

with open(data_file, "r", encoding='ANSI') as f:
    data = f.read()

#for colum numbers from below line, -2
#01/07/2023 00:00:03,0R0,Dn=095D,Dm=274D,Dx=352D,Sn=0.3M,Sm=5.8M,Sx=9.6M,Ta=17.9C,Ua=73.7P,Pa=1.0058B,Rc=13.02M,Rd=12480s,Ri=0.0M,Hc=0.0M,Hd=0s,Hi=0.0M,Th=18.0C,Vh=12.1N,Vs=12.1V,Vr=3.631V

#first line boundaries
line_start = 0
line_end = 187

#line without new line char. - COULD MAKE THIS AN INSTANCE OF RECORD CLASS
line = data[line_start:line_end]
date = line[0:10]
time = line[11:19]

#COULD CREATE A RECORD CLASS WITH BELOW AS ATTRIBUTES?
#   https://docs.python.org/3/tutorial/classes.html
#   https://www.w3schools.com/python/python_classes.asp
#find e.g. "Rc" in string, get value between "=" and ","
rain_accum = data[line.find("Rc")+3:line.find(",",line.find("Rc"))-1]
rain_dur = data[line.find("Rd")+3:line.find(",",line.find("Rd"))-1]
rain_inten = data[line.find("Ri")+3:line.find(",",line.find("Ri"))-1]
air_temp = data[line.find("Ta")+3:line.find(",",line.find("Ta"))-1]
supply_V = data[line.find("Vs")+3:line.find(",",line.find("Vs"))-1]
ref_V = data[line.find("Vr")+3:line.find(",",line.find("Vr"))-1]

invalid_line = find_next_bad_record(data, line)

next_valid_line = find_next_good_record(data, line)

#for testing get_next_line
line_start, line_end = get_next_line(len(line)-1, data)
line = data[line_start:line_end]


line_start, line_end = get_next_line(len(line)-1, data)
line = data[line_start:line_end]


line_start, line_end = get_next_line(len(line)-1, data)
line = data[line_start:line_end]


#if previous record to invalid_line is within half an hour(THIS CAN CHANGE),
# get records from previous 2 hours every 5 minutes(THESE CAN ALSO CHANGE) up to last valid record,
# use these records to chart rainfall

#if following record to next_valid_line is within 5 mins,
# get records for next 2 hours every 5 mins,
# chart rainfall

#chart scraped data to compare and fill in the gaps

f.close()
