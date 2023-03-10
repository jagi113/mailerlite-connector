from dotenv import load_dotenv
import os
import json
import asyncio
import aiohttp
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )


def check_response_status(response):
    if response.status == 401:
        logging.critical(
            "Connection was not established! Make sure your API TOKEN is correct!")
    elif response.status == 400:
        logging.critical(response["error"]["message"])
    elif response.status == 404:
        logging.critical(response["error"]["message"])



class MailerLite():
    def __init__(self, API_TOKEN: str):
        self.API_TOKEN = API_TOKEN
        self.payload = []
        self.validate_api_token()

    # METHODS FOR SENDING REQUESTS

    async def make_requests(self) -> list:
        async with aiohttp.ClientSession() as session:
            requests = self.create_requests(session)

            try:
                responses = await asyncio.gather(*requests)
            except aiohttp.ClientConnectorError as e:
                logging.critical(f"Connection Error: {str(e)}")
                responses = []

            results = []
            for response in responses:
                check_response_status(response)
                
                try:
                    result = await response.json()
                    results.append(result)
                    logging.info(result)
                except Exception as e:
                    logging.critical(f"Failed to get JSON response: {str(e)}")
                    results.append({})

            return results

    def create_requests(self, session: aiohttp.ClientSession) -> list:
        requests = []
        for i in range(len(self.payload)):
            version = {
                "base_api_url": "https://api.mailerlite.com/api/v2/",
                "headers": {
                    "Content-Type": "application/json",
                    "X-MailerLite-ApiKey": self.API_TOKEN
                }
            }

            url = version["base_api_url"]+self.payload[i]["url_path"]

            try:
                if self.payload[i]["method"] == "get":
                    requests.append(session.get(
                        url, headers=version["headers"]))
                elif self.payload[i]["method"] == "post":
                    requests.append(session.post(url, data=json.dumps(self.payload[i]["data"]), headers=version["headers"],
                                                 ))
            except Exception as e:
                logging.critical(f"Failed to create request: {str(e)}")
        return requests

    def send_to_api(self) -> list:
        try:
            final_responses = asyncio.run(self.make_requests())
        except Exception as e:
            logging.critical("Failed to make requests", exc_info=True)
            final_responses = []

        self.payload.clear()

        return final_responses


    def validate_api_token(self) -> None:
        self.establish_connection()
        response = self.send_to_api()
        if "account" in response[0]:
            logging.info("API TOKEN is correct!")
        

    # METHODS FOR CREATING PAYLOAD REQUESTS
    # Establishing connection
    def establish_connection(self) -> None:
        self.payload.append({
            "method": "get",
            "url_path": "me",
        })

    # Listing subscribers
    def list_subscribers(self) -> None:
        self.payload.append({
            "method": "get",
            "url_path": "subscribers",
        })

    # Creating subscribers
    def create_subscriber(self, subscriber_name: str, subscriber_email: str) -> None:
        self.payload.append({
            "method": "post",
            "url_path": "subscribers",
            "data": {
                "email": subscriber_email,
                "name": subscriber_name,
                "fields": {
                    "last_name": subscriber_name.split()[-1]
                }
            }
        })

    # Getting group info by name
    def get_group(self, group_name: str) -> None:
        self.payload.append({
            "method": "post",
            "url_path": "groups/search",
            "data": {"group_name": group_name}
        })

    # Creating a new group
    def create_group(self, group_name: str) -> None:
        self.payload.append({
            "method": "post",
            "url_path": "groups",
            "data": {"name": group_name}
        })

    # Adds a new single subscriber to the group with the given name. If the group or subscriber doesn't exist, it gets created.
    # If multiple groups with the same name exist, the subscriber is added to the oldest group.
    def assign_group_subscriber(self, subscriber_name: str, subscriber_email: str, group_name: str) -> None:
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

    # For testing purposes
    mailerlite_account = MailerLite(API_TOKEN)
    # mailerlite_account.create_subscriber("Jason Crazy2", "jason@mail.com2")
    # mailerlite_account.create_group("class_group")
    # mailerlite_account.assign_group_subscriber("Dummy3", "dummy3@mail.com", 3)

    # results = mailerlite_account.send_to_api()

    # jresults = json.dumps(results, indent=2)
    # with open("output.json", "w") as output:
    #     output.write(jresults)
