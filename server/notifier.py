# server/notifier.py

import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

import requests
from shared.utils import PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN

def send_pushover_notification(message, priority=0, title="New Politicians Action"):
    url = 'https://api.pushover.net/1/messages.json'
    params = {
        'token': PUSHOVER_API_TOKEN,
        'user': PUSHOVER_USER_KEY,
        'message': message,
        'title': title,
        'priority': priority
    }
    try:
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print('Notification sent successfully')
        else:
            print(f"Failed to send notification: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")