# This program monitors the web page for changes and sends an email if there is a change in the count of items appearing on the page.

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# URL of the web page to be monitored
URL = "https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&fuelId%5B%5D=1&fuelId%5B%5D=3&last=3&priceTo=6000&conditions%5B%5D=4&conditions%5B%5D=1&locationId=4&radius=3"#input('Enter the URL of the web page to be monitored: ')

# Email address of the sender
sender = input('Enter your email address: ')
# Email address of the receiver
receiver = input('Enter the email address of the receiver: ')
# Password of the sender's email address
password = input('Enter the password of the sender\'s email address: ')

# Headers to be sent with the request
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

# Function to check the number of items on the page
def check_items():
    # Get the HTML of the page
    page = requests.get(URL, headers=headers)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find all the items
    items = soup.find_all('div', class_="mdc-card__primary-action")
    # The name of the newest item
    item_name = (items[0].find('a').find('h5', class_='card__title mdc-typography mdc-typography--headline5 observable').text).replace('\n', '').strip()
    # The price of the newest item
    item_price = (items[0].find('a').find('div').text).replace('\n', '').strip()
    # Message 
    message = 'The newest item is: ' + item_name + ' for ' + item_price
    # Return the number of items
    return len(message)

# Function to send an email
def send_mail():
    # Email address of the sender
    global sender
    # Email address of the receiver
    global receiver
    # Password of the sender's email address
    global password
    # SMTP server address
    smtp_server = 'smtp.office365.com'
    # SMTP server port
    port = 587
    # Subject of the email
    subject = check_items()
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

    print('Email sent!')
    

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
            items = new_items

# Main function
def main():
    # Check if the number of items has changed
    send_mail()

# Run the main function
if __name__ == '__main__':
    main()