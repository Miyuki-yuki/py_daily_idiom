# filename: daily_idiom.py

import smtplib
import argparse
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# .env file upload
load_dotenv()
# List of idioms, their meanings, and example sentences
idioms = [
    {"idiom": "Break a leg", "meaning": "Good luck", "example": "Break a leg in your new job!"},
    {"idiom": "Bite the bullet", "meaning": "To get an unpleasant task over with", "example": "I bit the bullet and finally cleaned my messy room."},
    {"idiom": "Barking up the wrong tree", "meaning": "To have a false idea about something", "example": "If you think I'm going to do your homework for you, you're barking up the wrong tree."},
    # Add more idioms here...
]

# Gmail account details
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('sv13199.xserver.jp', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to, text)
        server.quit()
        print('Email sent!')
    except Exception as e:
        print('Something went wrong...', e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="The recipient email address")
    parser.add_argument("start_date", help="The start date in YYYY-MM-DD format")
    parser.add_argument("end_date", help="The end date in YYYY-MM-DD format")
    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    delta = end_date - start_date

    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        idiom = idioms[i % len(idioms)]
        subject = f"Idiom of the day for {date.strftime('%Y-%m-%d')}"
        body = f"Idiom: {idiom['idiom']}\nMeaning: {idiom['meaning']}\nExample: {idiom['example']}"
        send_email(args.email, subject, body)

if __name__ == "__main__":
    main()