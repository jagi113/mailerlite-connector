from dotenv import load_dotenv
import os

import json
import asyncio
import aiohttp

import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

logging.debug('Here you have some information for debugging.')
logging.info('Everything is normal. Relax!')
logging.warning('Something unexpected but not important happend.')
logging.error('Something unexpected and important happened.')
logging.critical('OMG!!! A critical error happend and the code cannot run!')




# METHODS FOR CREATING PAYLOAD
# Creating subscribers
def list_subscribers(API_TOKEN): 
  return {
    "API_TOKEN": API_TOKEN,
    "method": "get",
    "url_path": "subscribers",
  }


# Creating subscribers
def create_subscriber(API_TOKEN, subscriber_name: str, subscriber_email): 
  return {
    "API_TOKEN": API_TOKEN,
    "method": "post",
    "url_path": "subscribers",
    "data": {
      "email": subscriber_email,
      "name": subscriber_name,
      "fields": {
        "last_name" : subscriber_name.split()[-1]
      }
    }
  }


# Getting group info by name
def get_group(API_TOKEN, group_name): 
  return {
    "API_TOKEN": API_TOKEN,
    "method": "post",
    "url_path": "groups/search",
    "data": {"group_name" : group_name}
  }


# Creating a new group
def create_group(API_TOKEN, group_name): 
  return {
    "API_TOKEN": API_TOKEN,
    "method": "post",
    "url_path": "groups",
    "data": {"name" : group_name}
  }     
  

# Add a new single subscriber to the group with the given name. If the group or subscriber doesn't exist, it gets created. 
# If multiple groups with the same name exist, the subscriber is added to the oldest group.
def assign_group_subscriber(API_TOKEN, subscriber_name, subscriber_email, group_name): 
  return {
    "API_TOKEN": API_TOKEN,
    "method": "post",
    "url_path": "groups/group_name/subscribers",
    "data": {
      "group_name": group_name, 
      "email": subscriber_email, 
      "name": subscriber_name
      }
  }    




# MAIN FUNCTIONS SECTION

def create_requests(session, payload):
  requests = []
  for i in range(len(payload)):
    version = {
      "base_api_url" : "https://api.mailerlite.com/api/v2/",
      "headers" : {
        "Content-Type": "application/json",
        "X-MailerLite-ApiKey": payload[i]["API_TOKEN"]
      }
    }
    url = version["base_api_url"]+payload[i]["url_path"]
    if payload[i]["method"] == "get":
      requests.append(session.get(
        url, 
        headers=version["headers"]
        ))
    elif payload[i]["method"] == "post":
      requests.append(session.post(
        url, 
        data=json.dumps(payload[i]["data"]), 
        headers=version["headers"],
        ))
  return requests


# Main function
async def send_to_api(payload):
  
  async with aiohttp.ClientSession() as session:
    
    requests = create_requests(session, payload)
    responses = await asyncio.gather(*requests)

    results = [ await response.json() for response in responses]
  return results




if __name__ == "__main__":
  load_dotenv()
  API_TOKEN = os.getenv("API_TOKEN")
  
  # For our purposes we need to feed payload with following functions:
  # For creating a subscriber: api_create_subscriber(subscriber_name, subscriber_email)
  # For creating a tag/group: api_create_group(group_name)
  # For creating or just assigning a subscriber to a (new or existing) tag/group: api_assign_group_subscriber(subscriber_name, subscriber_email, group_name)
  payload = [assign_group_subscriber(API_TOKEN, "Jaroslav Girovsky", "jaroslavgirovsky@gmail.com", "jason_group"), 
            create_subscriber(API_TOKEN, "Jason Crazy", "jason@mail.com"), 
            create_group(API_TOKEN, "jason_group"), 
            assign_group_subscriber(API_TOKEN, "Jason Crazy", "jason@mail.com", "jason_group"), 
            assign_group_subscriber(API_TOKEN, "someone", "someone@mail.com", "something"),]
    
  results = asyncio.run(send_to_api(payload))
  jresults = json.dumps(results, indent=2)
  with open("output.json", "w") as output:
    output.write(jresults)
