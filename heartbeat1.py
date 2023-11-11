#!/usr/bin/python3

# Import the required modules
import os # For accessing environment variables
import time # For sleeping between pings
import requests # For sending HTTP requests to the server
import smtplib # For sending emails via SMTP protocol
import logging # For logging messages to files or console
import argparse # For parsing command-line arguments
import configparser # For reading config files in INI format


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Monitor server status and send email alert if down.') # Create an argument parser object with a description of the script
parser.add_argument('-c', '--config', type=str, default='/etc/supervisor/conf.d/heartbeat.conf',
help='Path to config file containing server URL, email credentials, etc.') # Add an optional argument for the path to the config file with a short and long option name, a type, a default value and a help message
args = parser.parse_args() # Parse the arguments given by the user and store them in a namespace object

# Create a config parser object
config = configparser.ConfigParser() # Create a config parser object that can read and write config files in INI format

# Read config file
config.read(args.config) # Read the config file from the path given by the user or the default value and store the data in the config parserobject

# Access the config data by sections and keys
server_url = config["server"]["url"] # The URL of the server to monitor
email_from = config["email"]["from"] # The email address to send the alert from
email_to = config["email"]["to"] # The email address to send the alert to
email_subject = config["email"]["subject"] # The subject of the email alert
email_body = config["email"]["body"].format(server_url=server_url) # The body of the email alert with the server URL inserted
email_password = config["email"]["password"] # The password of the email account
email_username = config["email"]["username"] # The username of the email account
log_file = config["logging"]["log_file"] # The name of the log file
error_file = config["logging"]["error_file"] # The name of the error file

# Set up logging
error_handler = logging.FileHandler(error_file) # Create a file handler for logging
error_handler.setLevel(logging.ERROR) # Set the level of the error handler to ERROR

logging.basicConfig( # Configure the basic settings for logging
        level=logging.INFO, # Set the level of the logger to INFO
        format='%(asctime)s %(levelname)s %(message)s', # Set the format of the log messages
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file), # Add a file handler for logging general messages
            error_handler # Add the error handler
        ]
)

# Define ping interval in seconds
PING_INTERVAL = 5

# Define function to ping server
def ping_server():
    logging.info(f"Pinging {server_url}...") # Log an info message before pinging
    try:
        response = requests.get(server_url) # Send a GET request to the server URL and store the response object
        if  response.status_code !=200: # Check if the status code of the response is not 200 (OK)
            raise Exception("Server down") # Raise an exception with a custom message
        logging.info(f"Pinged {server_url} successfully.") # Log an info message after pinging successfully
    except requests.exceptions.ConnectionError as e: # Handle the exception that occurrs when failing to connect to the server URL
        logging.error(f"Failed to connect to {server_url}: {e}") # Log an error message with the exception details
        def send_email() # Call the function to send an email alert
    except Exception as e: # Handle any other exception that may occur during pinging
        logging.error(f"An error occurred: {e}") # Log an error message with the exception details
        def send_email() # Call the function to send an email alert

import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import logging

# Define function to send email
SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
flow = InstalledAppFlow.from_client_secrets_file('oath.json', SCOPES)
creds = flow.run_console()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s -%(levelname)s - %(message)s')

# Create and connect to the service object using a context manager
with build('gmail', 'v1', credentials=creds) as service:
    message = MIMEText('This is the body of the email')
    message['to'] = 'recipient@gmail.com'
    message['subject'] = 'Email Subject'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        logging.info('sent message to {0} Message Id: {1}'.format(message, message["id"]))
    except HTTPError as error:
        logging.error('An error occurred: {0}'.format(error))
        message = None

# Start script
logging.info("Script started") # Log an info message at the start of the script

# Ping server in a loop
while True:
    ping_server() # Call the function to ping the server
    time.sleep(PING_INTERVAL) # Wait for the ping interval before pinging again




