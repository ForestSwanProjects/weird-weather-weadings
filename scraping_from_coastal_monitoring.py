#only needs to be run once as we are not looking at live data or data that will change
#to do: 1) add urls to file_paths.json, 2) add func to create records.txt in directory from .json, 3) write records to csv

import os
import json
import requests as req
from bs4 import BeautifulSoup as beausoup

def not_charts_header(tag):
    return tag.name("tr") and not tag.has_attr("class")

### START

with open("file_paths.json") as paths:
    paths_dict = json.load(paths)


#user chooses which records to get
user_choice = input("[1] - get Exeter records\n[2] - get West Bay Harbour results\n-> ")

if user_choice == "1":

    records_file = paths_dict["ex_records_file"]

    url_list = ["https://coastalmonitoring.org/realtimedata/?user_indate=08-07-2023&chart=117&tab=met&disp_option=1&datum=chart&range=week&submit=Go&website2=","https://coastalmonitoring.org/realtimedata/?user_indate=01-07-2023&chart=117&tab=met&disp_option=1&datum=chart&range=week&submit=Go&website2="]

elif user_choice == "2":

    records_file = paths_dict["wb_records_file"]

    url_list = ["https://coastalmonitoring.org/realtimedata/?user_indate=08-07-2023&chart=95&tab=met&disp_option=1&datum=chart&range=week&submit=Go&website2=","https://coastalmonitoring.org/realtimedata/?user_indate=01-07-2023&chart=95&tab=met&disp_option=1&datum=chart&range=week&submit=Go&website2="]


f = open(records_file, "w")

#webscraping bit
for url in url_list:

    page = req.get(url, verify=False)
    soup = beausoup(page.content, "html.parser")

    boxbody = soup.body.find("div", class_="boxbody")
    table_body_tag = boxbody.find_all("table", class_="table table-striped")
    records = table_body_tag[1].find_all("tr", class_=None)

    for i in range(len(records)-1):
        curr_rec = records[i].find_all('td')
        record_string = ""
        for j in range(len(curr_rec)-1):
            if j == 10:
                curr_data = curr_rec[j].get_text() + "\n"
            else:
                curr_data = curr_rec[j].get_text() + ","
            record_string = record_string + curr_data
        f.write(record_string)

f.close()