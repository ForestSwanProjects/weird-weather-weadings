#only needs to be run once as we are not looking at live data or data that will change
#to do: 1) add urls to file_paths.json, 2) add func to create records.txt in directory from .json

import os
import json
import requests as req
from bs4 import BeautifulSoup as beausoup

def not_charts_header(tag):
    return tag.name("tr") and not tag.has_attr("class")

### START

with open("file_paths.json") as paths:
    paths_dict = json.load(paths)

records_file = paths_dict["records_file"]

f = open(records_file, "w")

#webscraping bit
url_list = ["https://coastalmonitoring.org/realtimedata/?user_indate=01-07-2023&chart=117&tab=met&disp_option=1&datum=chart&range=week&submit=Go&website2=","https://coastalmonitoring.org/realtimedata/?user_indate=08-07-2023&chart=117&tab=met&disp_option=1&datum=chart&range=week&submit=Go&website2="]

for url in url_list:

    page = req.get(url)
    soup = beausoup(page.content, "html.parser")

    table_body_tag = soup.body.find("div", class="boxbody").find("div", class="table table-striped")

    records = table_body_tag.findall(not_charts_header)

    record_string = ""

    for i in range(0, len(records)-1):
        curr_rec = records[i].findall("td")
        for j in range(0, len(curr_rec)-1):
            if j == 11:
                curr_data = curr_rec[j].get_text() + "\n"
            else:
                curr_data = curr_rec[j].get_text() + ","
            record_string = record_string + curr_data
        f.write(record_string)

f.close()