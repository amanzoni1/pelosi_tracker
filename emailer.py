import time
from mailjet_rest import Client
from utils import MAILJET_API_KEY, MAILJET_SECRET_KEY, EMAIL_FROM, EMAIL_FROM_NAME
import os

mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

def send_email(to_emails, subject, html_content):
    messages = []
    for email in to_emails:
        messages.append({
            "From": {
                "Email": EMAIL_FROM,
                "Name": EMAIL_FROM_NAME
            },
            "To": [
                {
                    "Email": email,
                    "Name": email.split('@')[0]
                }
            ],
            "Subject": subject,
            "HTMLPart": html_content
        })

    data = {
        'Messages': messages
    }

    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        print(f"Email sent to {', '.join(to_emails)}")
    else:
        print(f"Failed to send email: {result.status_code}, {result.json()}")

def send_bulk_emails(recipient_emails, subject, html_content):
    batch_size = 200  # Adjust based on Mailjet's limits
    for i in range(0, len(recipient_emails), batch_size):
        batch_emails = recipient_emails[i:i+batch_size]
        send_email(batch_emails, subject, html_content)
        time.sleep(1)

def generate_email_content(analysis_result, last_name):
    # Load the email template
    with open(os.path.join('templates', 'email_template.html'), 'r') as file:
        template = file.read()
    # Replace placeholders with actual content
    html_content = template.replace('{{last_name}}', last_name).replace('{{analysis_result}}', analysis_result)
    return html_content

def get_recipient_emails():
    subscribers = []
    subscribers_file = os.path.join('web_app', 'subscribers.txt')
    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as f:
            subscribers = [line.strip() for line in f if line.strip()]
    return subscribers