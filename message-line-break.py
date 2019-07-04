import requests

url = "https://api.helpshift.com/v1/YOUR-DOMAIN/issues/2022/messages"

payload = "message-type=Text&message-body=line break%0Atest"
headers = {
    'Authorization': "Basic XXXXXXXXXX",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    'Accept': "*/*",
    'Host': "api.helpshift.com",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)