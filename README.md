##Mailerlite Connector

It is simple API async connector to connect to MailerLite account.

It uses aiohttp and asyncio.

Class is called MailerLite.  
Instance is created by providing API_TOKEN.  
Class has several methods for creating requests like:  
For creating a subscriber: create_subscriber(subscriber_name, subscriber_email)  
For creating a tag/group: create_group(group_name)  
For creating or just assigning a subscriber to a (new or existing) tag/group: assign_group_subscriber(subscriber_name, subscriber_email, group_name)

Method for sending created requests is "send_to_api()"

MailerLite has 2 API endpoints:  
V1 - supports all accounts but rate limit is only 60 requests per minute  
V2 - supports only accounts created after March 22th 2022 but rate limit is up to 120 requests

async_connector_v1.py uses API V1

Very developed Python Wrapper for Mailerlite API (handles V1) can be found at https://github.com/skoudoro/mailerlite-api-python
