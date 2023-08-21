# Program to extract and format raw data from weather station

import json

with open("file_paths.json", encoding="UTF-8") as paths_file:
    paths_dict = json.load(paths_file)

data_file = open(paths_dict["raw_data"], "r")
data = data_file.read()

print(data[-1])

print(data_file.readline())
print(data_file.readline())