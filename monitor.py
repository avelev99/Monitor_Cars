# This program monitors the web page for changes and sends an email if there is a change in the count of items appearing on the page.

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# URL of the web page to be monitored
URL = input('Enter the URL of the web page to be monitored: ')

# Headers to be sent with the request
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

# Function to send an email
def send_mail():
    # Email address of the sender
    sender = input('Enter your email address: ')
    # Email address of the receiver
    receiver = input('Enter the email address of the receiver: ')
    # Password of the sender's email address
    password = input('Enter the password of the sender\'s email address: ')
    # SMTP server address
    smtp_server = 'smtp.gmail.com'
    # SMTP server port
    port = 587
    # Subject of the email
    subject = 'Number of items has changed!'
    # Body of the email
    body = 'Check the link: ' + str(URL)
    # Message to be sent
    message = f'Subject: {subject}\n\n{body}'
    # Create a SMTP session
    session = smtplib.SMTP(smtp_server, port)
    # Start TLS for security
    session.starttls()
    # Authentication
    session.login(sender, password)
    # Sending the mail
    session.sendmail(sender, receiver, message)
    # Terminating the session
    session.quit()
    
# Function to check the number of items on the page
def check_items():
    # Get the HTML of the page
    page = requests.get(URL, headers=headers)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find all the items
    items = soup.find_all('div', class_='car-item')
    # Return the number of items
    return len(items)

# Function to check if the number of items has changed
def check_change():
    # Get the number of items
    items = check_items()
    while True:
        # Wait for 5 minutes
        time.sleep(300)
        # Get the number of items again
        new_items = check_items()
        # If the number of items has changed, send an email
        if items != new_items:
            send_mail()

# Main function
def main():
    # Check if the number of items has changed
    check_change()

# Run the main function
if __name__ == '__main__':
    main()