import requests

url = "https://api.helpshift.com/v1/YOUR-DOMAIN/issues"

message = "-body=python%0Atest"

payload = "platform-type=web&email=ted%40helpshift.com&message-body=python%0Atest"
headers = {
    'Authorization': "Basic XXXXXX",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    'Accept': "*/*",
    'Host': "api.helpshift.com",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)