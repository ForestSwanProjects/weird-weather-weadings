"""
Get a list of rainfall values from a nearby station around the times of each bad record.
"""

import pandas as pd
import time
import json
import datetime as dt

with open("file_paths.json") as paths:
    paths_dict = json.load(paths)

#get file paths
bad_lines_f = paths_dict["bad_data"]
full_data_f = paths_dict["wb_records_file"]

bad_df = pd.read_csv(bad_lines_f)

full_df = pd.read_csv(full_data_f)
full_df = full_df.iloc[::-1]#reverse order of rows to have them ordered by date ascendings
full_df = full_df.set_axis(['date/time','air press','wind spd (knts)','wind spd (m/s)','gust spd (knts)','gust speed (m/s)','wind dir','air temp','rainfall (mm)','rad','UV'], axis=1)
full_df = full_df.drop(columns=['air press','wind spd (knts)','wind spd (m/s)','gust spd (knts)','gust speed (m/s)','wind dir','rad','UV'], axis=1)

"""
for each invalid line:
    get rainfall every ten minutes over prev 2 hours
    get rainfall for every ten mins until time of next valid record
    get rainfall for every ten mins for following hour

    chart somehow

"""
rainfalls = []

for i, row_i in bad_df.iterrows():

    #get record of bad line and its date and time
    bad_rec = row_i["invalid"]
    br_date_time = bad_rec[0:19]
    
    #round minute to nearest ten minutes
    mins = str(round(int(br_date_time[14:16]), -1))
    hrs = br_date_time[11:13]

    if mins == "60":
        mins = "00"
        hrs = str(int(br_date_time[11:13]) + 1).zfill(2)

    #drop seconds as they aren't included in other dataset
    br_date_time = br_date_time[:11] + hrs + ":" + mins

    #match to fit format of records_file.csv
    br_date_time = br_date_time.replace("/","-")
    br_dt = dt.datetime.strptime(br_date_time, "%d-%m-%Y %H:%M")

    #get time of 2 hours before
    minus_2_hr = br_dt - dt.timedelta(hours=2)

    #get time of 1 hour after
    plus_1_hour = br_dt + dt.timedelta(hours=1)

    #init list of rainfall values
    rainfall_vals = []

    #get rainfall values between set times
    for j, row_j in full_df.iterrows():

        if minus_2_hr <= dt.datetime.strptime(row_j["date/time"], "%d-%m-%Y %H:%M") < plus_1_hour:

            rainfall_vals.append(row_j["rainfall (mm)"])

    rainfalls.append((br_date_time, rainfall_vals))


#get list of records that were corrupted when it rained around the time
wet_list = []

for j in rainfalls:
    for k in j[1]:
        if k != 0.0:
            if j not in wet_list:
                wet_list.append(j)

print(wet_list)

print("-"*50)

#get list of every time where it rained
wet_rows = []

for m, row_m in full_df.iterrows():
    if row_m["rainfall (mm)"] != 0.0:
        wet_rows.append((row_m["date/time"], row_m["rainfall (mm)"]))

print(wet_rows)