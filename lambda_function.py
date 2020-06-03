import json
import urllib3
import os
from base64 import b64encode

def lambda_handler(event, context):
    
    # Create Lambda Enviorment Variables with your HS Domain and API Key
    HELPSHIFT_API_KEY = os.environ.get("HELPSHIFT_API_KEY")
    HS_DOMAIN = os.environ.get("HS_DOMAIN")
    encoded_credentials = b64encode(bytes(f'{HELPSHIFT_API_KEY}:""',
                            encoding='ascii')).decode('ascii')
    
    # Declare Variables from HS Bot
    issue_id = event['issue_id']
    user_id = event['user_id']
    
    http = urllib3.PoolManager()
    
    # PUT API CALL TO YOUR SYSTEM HERE 
    # I used urllib3 since it has native support in Lambda
    '''request1 = http.request(
        'GET',
        'https://YOUR API',
        headers={'YOUR_KEY': 'YOUR VALUES'},
        fields=encoded_body)
    
    result1 = json.loads(request1.data.decode('utf-8'))
    
    if request1.status != 200:
        raise Exception(
            print("GET Call To Your CRM API Failed: ", request1.data.decode('utf-8'))
            )'''
            
    # Map Responses from API call to your CRM to variables to send to the HS-API 
    #result1 = json.loads(r.data.decode('utf-8'))
    #your_CIF = result1["customer"]["customerData"]
    
    # POST TO HS-API
    request2 = http.request('PUT', 'https://api.helpshift.com/v1/{}/issues/{}'.format(HS_DOMAIN, issue_id),
                body= 'custom_fields={\"YOUR_CIF_API_NAME\": {\"type\":\"singleline\", \"value\":\"%s\"}}'% (your_CIF),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'authorization': 'Basic {}'.format(encoded_credentials)
                })

    if request2.status != 200:
        raise Exception(
            print("Your PUT to HS-API Failed: ", request2.data.decode('utf-8'))
            )

    return {
        'statusCode': 200,
        'body': json.dumps({'success':True})
    }
