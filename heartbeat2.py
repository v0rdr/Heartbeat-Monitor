#!/usr/bin/env python3

# Import modules
import requests
import time
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage
import base64

# Define constants
SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
    ]
SERVER_URL = "http://lskdjflkasfjfhneu.com" # The URL of the server to ping
PING_INTERVAL = 5 # The interval in seconds between each ping
MAX_FAILURES = 2 # The maximum number of failed pings before sending an email notification
SENDER = "testtesytesto@gmail.com" # The sender's email address
RECIPIENT = "kristofersimpson@outlook.com" # The recipient's email address
SUBJECT = "LAWD! ZE SERVER IS DOWN!" # The subject of the email notification
BODY = f"The server: {SERVER_URL} is down. Please check on that beauty ASAP." # The body of the email notification

# Set up logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Define a function to ping the server and return the status code
def ping_server():
    try:
        # Make a GET request to the server
        response = requests.get(SERVER_URL)
        # Return the status code
        return response.status_code
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        logging.error(f'Failed to ping the server: {e}')
        # Return None to indicate an error
        return None

# Define a function to send an email using the Gmail API
def send_email(sender, recipient, subject, body):
    try:
        # Create a server object for the Gmail API
        service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
        # Create an EmailMessage object
        msg = EmailMessage()
        # Set the email headers
        msg['From'] = SENDER
        msg['To'] = RECIPIENT
        msg['Subject'] = SUBJECT
        # Set the email content
        msg.set_content(BODY)
        # Encode the message as a base64url string
        message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        # Send the message using the Gmail API
        response = service.users().messages().send(userId='me', body={'raw': message}).execute()
        # Log the message ID and thread ID
        logging.info(f'Message ID: {response["id"]}')
        logging.info(f'Thread ID: {response["threadId"]}')
    except Exception as e:
        # Handle any other errors
        logging.error(f'Failed to send email: {e}')

# Define a function to run the main logic of the script
def main():
    # Initialize a counter for failed pings
    failures = 0
    # Start an infinite loop
    while True:
        # Ping the server and get the status code
        status = ping_server()
        # Check if the status code is 200 (OK)
        if status == 200:
            # Log a success message
            logging.info('Server is up and running')
            # Reset the counter for failed pings
            failures = 0
        else:
            # Log an error message with the status code or the exception message
            logging.error(f'Server is down with status code {status}')
            # Increment the counter for failed pings
            failures += 1
            # Check if the counter has reached the maximum umber of failures
            if failures == MAX_FAILURES:
                # Send an email notification to the recipient
                send_email(SENDER, RECIPIENT, SUBJECT, BODY)
                # Log a notification message
                logging.info(f'Sent an email notification to {RECIPIENT}')
                # Reset the counter for failed pings
                failures = 0

        # Wait for the specified interval before pinging again
        time.sleep(PING_INTERVAL)

# Check if the script is executed directly and not imported by another module
if __name__ == '__main__':
    # Run the OAuth 2.0 authorization flow and get the credentials object
    flow = InstalledAppFlow.from_client_secrets_file('oath.json', SCOPES)
    creds = flow.run_local_server()
    # Run the main function
    main()
