##Mailerlite Connector

It is simple API sync connector to connect to MailerLite account.

MailerLite has 2 API endpoints:
V1 - supports all accounts but rate limit is only 60 requests per minute
V2 - supports only accounts created after March 22th 2022

Therefore I created 2 connectors. For light task as listing all subscribers or creating a new one the difference is minimal.
There however might be bigger problems for more advanced features. I am not sure what tasks this connector should perform.
Currently connector can sign up a user to an ESP providing his name, last name and email address (created for testing purposes).
Very develeped Python Wrapper for Mailerlite API (handles V1) can be found at https://github.com/skoudoro/mailerlite-api-python

Question 1: What api endpoint should I work on? Or should I try to implement both?
Question 2: Are there any preferences or suggestions what package to use for making connector async?
