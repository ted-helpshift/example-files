import requests
import time
import datetime
import json
from base64 import b64encode


def get_timestamp_in_ms(date):
   return str(int(time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y").timetuple()) * 1e3))

#  Suply your start and end date Key from 
start_date = "06/20/2020"
end_date = "06/22/2020"

#  Suply your API Key from 
DOMAIN = "YOUR DOMAIN"
HELPSHIFT_API_KEY = "YOUR API KEY"


#Converting your Variables - Don't Change 
start_ts = get_timestamp_in_ms(start_date)
end_ts = get_timestamp_in_ms(end_date)
encoded_credentials = b64encode(bytes(f'{HELPSHIFT_API_KEY}:""',
                                encoding='ascii')).decode('ascii')

#CREATE A CSV FILE TO WRITE IDs 
f = open("ID-LIST.csv", "w")

while 1:

    headers = {
        'authorization': 'Basic {}'.format(encoded_credentials),
        }
    r = requests.get(
        ('https://api.helpshift.com/v1/'+ DOMAIN +'/issues?sort-by=creation-time&sort-order=asc&created_since='
        + start_ts + '&created_until=' + end_ts + '&page-size=1000'),
        headers= headers )
    data = r.json()
    print(r.text[0:200],"...")

    
    # All the issues for the given query
    issues = (data['issues'])
    
    if not issues:
        print("No issues. Done")
        break

    x = json.loads(r.text)
    
    #Write each ID to a CSV
    for item in x["issues"]:
        index = x["issues"].index(item)
        length = len(x["issues"]) - 1
        if str(item["redacted"]) == "False" and index != length:
            f.write("%s\n"%(item["id"]))
            
        if str(item["redacted"]) == "True" and index != length:
            print("Issue ID %s was redacted"%(item["id"]))
            f.write("%s\n"%(item["id"]))

    if len(issues) == 1:
        # This is the last issue process it.
        issues_to_be_processed = issues
    else:
        # Drop the last issue and process it in the next loop because created-since of last issue is taken and it will be
        # the first issue in the next query.
        issues_to_be_processed = issues[:-1]
    # issues_to_be_processed is the array which you should process it further like write to your external system etc.

    if len(issues) == 1:
        print('This is the only 1 issue in the chunk. Process it and you are done.')
        break

    start_ts = str(issues[-1]['created_at'])
    time.sleep(.75)
