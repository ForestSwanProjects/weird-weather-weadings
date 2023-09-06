import pandas as pd
import time
import json

with open("file_paths.json") as paths:
    paths_dict = json.load(paths)

#get file paths
bad_lines_f = paths_dict["bad_data"]
full_data_f = paths_dict["records_file"]

bad_df = pd.read_csv(bad_lines_f)

full_df = pd.read_csv(full_data_f)
full_df = full_df.set_axis(['date/time','air press','wind spd (knts)','wind spd (m/s)','gust spd (knts)','gust speed (m/s)','wind dir','air temp','rainfall (mm)','rad','UV'], axis=1)
full_df = full_df.drop(columns=['air press','wind spd (knts)','wind spd (m/s)','gust spd (knts)','gust speed (m/s)','wind dir','rad','UV'], axis=1)

print(bad_df.columns.values)
print(full_df.columns.values)

"""
for each invalid line:
    if prev line within half an hour
        get rainfall every ten minutes over prev 2 hours
    get rainfall for every ten mins until time of next valid record
    get rainfall for every ten mins for following hour

    chart somehow

"""

for i, row in bad_df.iterrows():
    bad_rec = row["invalid"]
