# shared/emailer.py

from mailjet_rest import Client
from .utils import MAILJET_API_KEY, MAILJET_SECRET_KEY, EMAIL_FROM, EMAIL_FROM_NAME
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

def send_transactional_email(to_email, subject, variables=None, is_template=True, template_id=None):
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
        "Subject": subject
    }

    if is_template:
        if not template_id:
            logger.error("Template ID must be provided for template-based emails.")
            return
        message["TemplateID"] = int(template_id)
        message["TemplateLanguage"] = True
        message["Variables"] = variables
    else:
        # For non-template emails, send the message as plain text
        message["TextPart"] = f"Message from {variables.get('user_name')} ({variables.get('user_email')}):\n\n{variables.get('message')}"

    data = {
        'Messages': [message]
    }
    
    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        logger.info(f"Email sent to {to_email}")
    else:
        logger.error(f"Failed to send email: {result.status_code}, {result.json()}")


def send_contact_email(name, email, message):
    subject = f"Contact Form Submission from {name}"
    recipients = 'a.manzoni14@gmail.com' 
    variables = {
        'user_name': name,
        'user_email': email,
        'message': message
    }
    # Send email as a regular (non-template) message
    send_transactional_email(recipients, subject, variables, is_template=False)