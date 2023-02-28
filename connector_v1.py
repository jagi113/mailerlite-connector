from dotenv import load_dotenv
import os

import json
import requests

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


section = "subscribers"

# Fields for subscriber creation 
email = "dummy2@mail.com"
name = "Dummy2"
last_name = "Stupid2"

# Example of data payload for mailerlite.com
data = {
    "email": email,
    "fields": {
      "name": name,
      "last_name": last_name,
    }
}

# Example of payload for mailerlite_connector
payload = {
  "API_TOKEN": API_TOKEN,
  "request": "get",
  "section": section,
  "data": data
}


def mailerlite_connector(payload = payload):
  
  # MAILERLITE VERSION SECTION
  # This is request setting for API V1
  # It is supported for all accounts, yet rate limits is 60 requests per minute 
  base_api_url = "https://api.mailerlite.com/api/v2/"
  headers={
      "Content-Type": "application/json",
      "X-MailerLite-ApiKey": payload["API_TOKEN"]
  }
  
  # Sending request section
  url = base_api_url+payload["section"]
  
  if payload["request"] == "get":
    response = requests.get(url, headers=headers)
  elif payload["request"] == "post":
    response = requests.post(url, data=json.dumps(payload["data"]), headers=headers)
  return(response.json())



if __name__ == "__main__":
  print(mailerlite_connector(payload))
