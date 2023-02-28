from dotenv import load_dotenv
import os

import json
import requests

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


section = "subscribers"

# fields for subscriber creation 
email = "dummy2@mail.com"
name = "Dummy2"
last_name = "Stupid2"

# example of data payload for mailerlite.com
data = {
    "email": email,
    "fields": {
      "name": name,
      "last_name": last_name,
    }
}

# example of payload for mailerlite_connector
payload = {
  "API_TOKEN": API_TOKEN,
  "request": "get",
  "section": section,
  "data": data
}

def mailerlite_connector(payload = payload):

  # mailerlite version section
  # this is request setting for API V2
  # it is supported for their accounts created after March 22nd, 2022, yet rate limits is 120 requests per minute 
  base_api_url = "https://connect.mailerlite.com/api/"
  headers={
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Authorization": f'Bearer {payload["API_TOKEN"]}',
  }
  
  # sending request section
  url = base_api_url+payload["section"]
  
  if payload["request"] == "get":
    response = requests.get(url, headers=headers)
  elif payload["request"] == "post":
    response = requests.post(url, data=json.dumps(payload["data"]), headers=headers)
  return(response.json())


if __name__ == "__main__":
  print(mailerlite_connector(payload))