from dotenv import load_dotenv
import os

import json
import asyncio
import aiohttp

import logging

logging.getLogger('asyncio').setLevel(logging.WARNING)

class MailerLite():
  def __init__(self, API_TOKEN:str):
          self.API_TOKEN = API_TOKEN
          self.payload = []

  # METHODS FOR SENDING REQUESTS
  def send_to_api(self):
    try:
      final_responses = asyncio.run(self.make_requests())
    except Exception as e:
      logging.critical("Failed to make requests", exc_info=True)
      final_responses = []

    for response in final_responses:
      if "error" in response:
        logging.critical(response["error"]["message"]) 

    self.payload.clear()
    return final_responses
  
  
  async def make_requests(self):
    async with aiohttp.ClientSession() as session:
      
      requests = self.create_requests(session)

      try:
        responses = await asyncio.gather(*requests)
      except aiohttp.ClientConnectorError as e:
        logging.critical(f"Connection Error: {str(e)}")
        responses = []
        
      results = []
      for response in responses:
        try:
          results.append(await response.json())
        except Exception as e:
          logging.critical(f"Failed to get JSON response: {str(e)}")
          results.append({})
          
      return results 

  
  
  def create_requests(self, session):
    requests = []
    for i in range(len(self.payload)):
      version = {
        "base_api_url" : "https://api.mailerlite.com/api/v2/",
        "headers" : {
          "Content-Type": "application/json",
          "X-MailerLite-ApiKey": self.API_TOKEN
        }
      }
      
      url = version["base_api_url"]+self.payload[i]["url_path"]

      try:
        if self.payload[i]["method"] == "get":
          requests.append(session.get(
            url, 
            headers=version["headers"]
            ))
        elif self.payload[i]["method"] == "post":
          requests.append(session.post(
            url, 
            data=json.dumps(self.payload[i]["data"]), 
            headers=version["headers"],
            ))
      except Exception as e:
        logging.critical(f"Failed to create request: {str(e)}")
    return requests   



  
  # METHODS FOR CREATING PAYLOAD REQUESTS
  # Listing subscribers
  def list_subscribers(self): 
    self.payload.append({
      "method": "get",
      "url_path": "subscribers",
    })


  # Creating subscribers
  def create_subscriber(self, subscriber_name: str, subscriber_email: str): 
    self.payload.append({
      "method": "post",
      "url_path": "subscribers",
      "data": {
        "email": subscriber_email,
        "name": subscriber_name,
        "fields": {
          "last_name" : subscriber_name.split()[-1]
        }
      }
    })


  # Getting group info by name
  def get_group(self, group_name: str): 
    self.payload.append({
      "method": "post",
      "url_path": "groups/search",
      "data": {"group_name" : group_name}
    })


  # Creating a new group
  def create_group(self, group_name: str): 
    self.payload.append({
      "method": "post",
      "url_path": "groups",
      "data": {"name" : group_name}
    })
  

  # Adds a new single subscriber to the group with the given name. If the group or subscriber doesn't exist, it gets created. 
  # If multiple groups with the same name exist, the subscriber is added to the oldest group.
  def assign_group_subscriber(self, subscriber_name: str, subscriber_email: str, group_name: str): 
    self.payload.append({
      "method": "post",
      "url_path": "groups/group_name/subscribers",
      "data": {
        "group_name": group_name, 
        "email": subscriber_email, 
        "name": subscriber_name
        }
    })  
      




if __name__ == "__main__":
  load_dotenv()
  API_TOKEN = os.getenv("API_TOKEN")
  
  # For our purposes we need to feed payload with following methods:
  # For creating a subscriber: create_subscriber(subscriber_name, subscriber_email)
  # For creating a tag/group: create_group(group_name)
  # For creating or just assigning a subscriber to a (new or existing) tag/group: assign_group_subscriber(subscriber_name, subscriber_email, group_name)
  
  mailerlite_account = MailerLite(API_TOKEN)
  mailerlite_account.create_subscriber("Jason Crazy2", "jason@mail.com2")
  mailerlite_account.create_group("class_group")
  mailerlite_account.assign_group_subscriber("Dummy3", "dummy3@mail.com", 3)
    
  results = mailerlite_account.send_to_api()
 

  jresults = json.dumps(results, indent=2)
  with open("output.json", "w") as output:
    output.write(jresults)
