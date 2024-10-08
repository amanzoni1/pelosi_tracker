# emailer.py
from mailjet_rest import Client
from utils import MAILJET_API_KEY, MAILJET_SECRET_KEY, EMAIL_FROM, EMAIL_FROM_NAME
import os

mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

def send_transactional_email(to_email, template_id, variables):
    message = {
        "From": {
            "Email": EMAIL_FROM,
            "Name": EMAIL_FROM_NAME
        },
        "To": [
            {
                "Email": to_email,
                "Name": to_email.split('@')[0]
            }
        ],
        "TemplateID": int(template_id),
        "TemplateLanguage": True,
        "Variables": variables
    }
    data = {
        'Messages': [message]
    }
    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        print(f"Email sent to {to_email}")
    else:
        print(f"Failed to send email: {result.status_code}, {result.json()}")