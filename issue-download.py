import requests
import time
import json
from base64 import b64encode

# Step 1: Enter your start and end date here
# You can get the data in epoch time here: https://www.epochconverter.com/
start_date = 1569801600000 # sept 2019
end_date = 1593056460000 #june 25 2020

#Constants - Don't change
DAY = 86400000
WEEK = 604800000

#Step 2 : pick your increment day or week
increment = WEEK
increment_name = "Week"

# Step 3 Suply your API Key from 
DOMAIN = "YOUR DOMAIN"
HELPSHIFT_API_KEY = "YOUR KEY"

# Don't change this - Convert API Key from Helpshift to Base 64
encoded_credentials = b64encode(bytes(f'{HELPSHIFT_API_KEY}:""',
                                encoding='ascii')).decode('ascii')

#CREATE A CSV FILE TO WRITE IDs 
f = open("ID-LIST.csv", "w")

#LOOP CODE 
while start_date < end_date:
    pages = 1
    i = 1
    readable_startdate = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(start_date/1000))
    
    while i <= pages:
        url = "https://api.helpshift.com/v1/%s/issues"%(DOMAIN)

        querystring = {
        # "languages":"{\"and\" : [\"en\"] }",
            "page-size":1000,
            "created_since": start_date,
            "created_until":  start_date + increment,
            "page":"%s"%(i)}

        headers = {
            'authorization': 'Basic {}'.format(encoded_credentials),
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text[0:100],"...")
        

        #GO THROUGH EACH ISSUE AND DO SOMETHING: 
        x = json.loads(response.text)
        pages = x["total-pages"]

        for item in x["issues"]:
            if str(item["redacted"]) == "False":
                f.write("%s\n"%(item["id"]))
            else:
                print("Issue ID %s was redacted"%(item["id"]))
                f.write("%s\n"%(item["id"]))
        print("----------- For %s Starting %s Write page %s of %s -----------"%(increment_name, readable_startdate, i, x["total-pages"]))
        time.sleep(.5)
        i += 1
    start_date += increment

print("------------------ Download Complete ------------------")
