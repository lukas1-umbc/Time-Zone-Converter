import requests
from bs4 import BeautifulSoup
import json

#grab the HTML from the webpage
url = 'https://www.timeanddate.com/time/zones/'
page = requests.get(url)

#use BS to easily read the HTML
soup = BeautifulSoup(page.content, 'html.parser')
rows = soup.find(id = 'tz-abb').find('tbody').find_all('tr')

#dictionary where each key is the TZ abbreviation and the value is the UTC offset
repeats = {}

#populate data so each element is a list, one for each time zone
data = []
for row in rows:

    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    tz = [ele for ele in cols if ele]

    #don't care about redundant time zones, e.g. ET when we already have EST and EDT
    #the offsets for these are written as UTC +x/-y
    if '/' not in tz[3]:
        data.append(tz)

    #need to deal with time zones that have the same abbreviations
    if tz[0] in repeats.keys():
        repeats[tz[0]] += 1
    else:
        repeats[tz[0]] = 1

#delete time zones in the repeats dict that have only one occurence
repeats = {key:val for key, val in repeats.items() if val > 1}

#write the contents of the data list into a json file, taking into account repeat abbreviations
#write repeat abbreviations like the following example:
#WST is both West Samoa Time (UTC +14) and Western Sahara Summer Time (UTC +0)
#West Samoa Time: WST UTC+14
#Western Sahara Summer Time: WST UTC+1
json_dict = {}
for tz in data:

    abbr = tz[0]
    offset = tz[3]

    #check if the abbreviation is a repeat
    #we exclude ACT because the zone it shared an abbreviation with was redundant, and PST because both zones named PST have the same offset
    if abbr in repeats and abbr != 'ACT' and abbr != 'PST':
        abbr = abbr + ' ' + offset.replace(' ', '')

    json_dict[abbr] = {'offset': offset}

#write the json file
with open('time_zones.json', 'w+') as f:
    json.dump(json_dict, f, indent=4)

