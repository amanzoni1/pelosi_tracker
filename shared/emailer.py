# shared/emailer.py

from mailjet_rest import Client
from .utils import MAILJET_API_KEY, MAILJET_SECRET_KEY, EMAIL_FROM, EMAIL_FROM_NAME, WELCOME_TEMPLATE_ID, UPDATE_TEMPLATE_ID, PURCHASE_TEMPLATE_ID, NEW_PSW_TEMPLATE_ID
from flask import url_for
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

# Function for sending the welcome email after registration
def send_welcome_email(user_email, user_name):
    subject = "Welcome to PoliticianTrade!"
    unsubscribe_link = url_for('unsubscribe.unsubscribe', email=user_email, _external=True)
    account_link = url_for('account', _external=True) 
    variables = {
        'user_name': user_name,
        'unsubscribe_link': unsubscribe_link,
        'account_link': account_link  
    }
    send_transactional_email(user_email, subject, variables, is_template=True, template_id=WELCOME_TEMPLATE_ID)

# Function for sending purchase confirmation
def send_purchase_email(user_email, user_name):
    subject = "Thank You for Subscribing to PoliticianTrade!"
    unsubscribe_link = url_for('unsubscribe.unsubscribe', email=user_email, _external=True)
    account_link = url_for('account', _external=True) 
    variables = {
        'user_name': user_name,
        'unsubscribe_link': unsubscribe_link,
        'account_link': account_link  
    }
    send_transactional_email(user_email, subject, variables, is_template=True, template_id=PURCHASE_TEMPLATE_ID)

# Function for sending monthly update email
def send_update_email(user_email, user_name, last_name, analysis_result):
    subject = f"PoliticianTrade Update: New Trade by {last_name}"
    unsubscribe_link = url_for('unsubscribe.unsubscribe', email=user_email, _external=True)
    variables = {
        'user_name': user_name,
        'last_name': last_name,
        'analysis_result': analysis_result,
        'unsubscribe_link': unsubscribe_link
    }
    send_transactional_email(user_email, subject, variables, is_template=True, template_id=UPDATE_TEMPLATE_ID)

# Function for sending password reset email
def send_password_reset_email(user_email, user_name, reset_link):
    subject = "Reset Your PoliticianTrade Password"
    unsubscribe_link = url_for('unsubscribe.unsubscribe', email=user_email, _external=True)
    variables = {
        'user_name': user_name,
        'reset_link': reset_link,
        'unsubscribe_link': unsubscribe_link
    }
    send_transactional_email(user_email, subject, variables, is_template=True, template_id=NEW_PSW_TEMPLATE_ID)

# Function for sending contact form email
def send_contact_email(name, email, message):
    subject = f"Contact Form Submission from {name}"
    recipients = 'info@politiciantrade.net' 
    variables = {
        'user_name': name,
        'user_email': email,
        'message': message
    }
    # Send email as a regular (non-template) message
    send_transactional_email(recipients, subject, variables, is_template=False)