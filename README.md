##Mailerlite Connector

It is simple API async connector to connect to MailerLite account.

It uses aiohttp and asyncio.

Payload is ged by functions:
For creating a subscriber: api_create_subscriber(subscriber_name, subscriber_email)
For creating a tag/group: api_create_group(group_name)
For creating or just assigning a subscriber to a (new or existing) tag/group: api_assign_group_subscriber(subscriber_name, subscriber_email, group_name)

MailerLite has 2 API endpoints:  
V1 - supports all accounts but rate limit is only 60 requests per minute  
V2 - supports only accounts created after March 22th 2022 but rate limit is up to 120 requests

async_connector_v1.py uses API V1

Code is still being improved.

Very developed Python Wrapper for Mailerlite API (handles V1) can be found at https://github.com/skoudoro/mailerlite-api-python
