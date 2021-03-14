import json
import datetime

#load the data from time_zones.json
with open('time_zones.json') as f:
    data = json.load(f)

#create a dictionary whose keys are the TZ abbreviations and the values are the offsets
tz_dict = {abbr:os for abbr,os in zip(data, [json_pair['offset'] for json_pair in [json_pair for json_pair in data.values()]])}

#given - the time zone to convert from [hour, minute, TZ, am/pm/24]
#target - the time zone to convert to (str)
def convert(given, target):

    #get all given info
    hour = given[0]
    min = given[1]
    tz = given[2]
    tod = given[3]

    #need to get the given time in a datetime() format
    #have to convert to 24 hour if in PM
    if tod == 'PM':
        hour = hour + 12
    
    given_dt = datetime.datetime(100, 1, 1, hour, min)

    #UTC offset for given TZ
    given_os = tz_dict[tz].split(' ')[1]
    if ':30' in given_os:
        given_os = int(given_os[:-3]) + 0.5
    else:
        given_os = int(given_os)

    #UTC offset for target TZ
    target_os = tz_dict[target].split(' ')[1]
    if ':30' in target_os:
        target_os = int(target_os[:-3]) + 0.5
    else:
        target_os = int(target_os)

    #the amount of time to add to the given time to get to the target time zone
    diff = target_os - given_os
    delta = datetime.timedelta(hours=diff)

    #add the difference and the given time to get the target time 
    new_time = given_dt + delta
    target_hour = new_time.hour  
    target_min = str(new_time.minute) + '0' if new_time.minute == 0 else str(new_time.minute) 
    target_tod = ''

    #convert back to 12 hour time if we have to
    if tod == 'AM' or tod == 'PM':
        #past noon, so we convert to 12 hour time
        #we don't need to do this if we want 12 hour time but the time is before noon; the number is the same
        if target_hour > 12:
            target_hour -= 12
            target_tod = 'PM'
        #AM/PM changes at noon so we need a special case
        elif target_hour == 12:
            target_tod = 'PM'
        #12 hour time, so we write midnight as 12:00, not 0:00
        elif target_hour == 0:
            target_hour = 12
            target_tod = 'AM'
        #otherwise the AM/PM is the same
        else:
            target_tod = tod

    return str(target_hour) + ':' + target_min + ' ' + target_tod
