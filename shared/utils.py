# shared/utils.py

import os
from dotenv import load_dotenv

# Determine the environment (production or development)
FLASK_ENV = os.getenv('FLASK_ENV', 'production')

# Load environment variables from .env file if it exists
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=ENV_PATH, override=False)

# Global constants
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

PUSHOVER_USER_KEY = os.environ.get('PUSHOVER_USER_KEY')
PUSHOVER_API_TOKEN = os.environ.get('PUSHOVER_API_TOKEN')

EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_FROM_NAME = os.environ.get('EMAIL_FROM_NAME')

MAILJET_API_KEY = os.environ.get('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.environ.get('MAILJET_SECRET_KEY')
WELCOME_TEMPLATE_ID = os.environ.get('MAILJET_WELCOME_TEMPLATE_ID')
UPDATE_TEMPLATE_ID = os.environ.get('MAILJET_UPDATE_TEMPLATE_ID')
PURCHASE_TEMPLATE_ID = os.environ.get('MAILJET_PURCHASE_TEMPLATE_ID')
NEW_PSW_TEMPLATE_ID = os.environ.get('MAILJET_NEW_PSW_TEMPLATE_ID')

DATABASE_URL = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')

# Base URL for scraping
BASE_URL = os.environ.get('BASE_URL', 'https://disclosures-clerk.house.gov/FinancialDisclosure')

# Directory to save PDFs
BASE_SAVE_DIR = os.path.join(PROJECT_ROOT, 'savedPdf')
os.makedirs(BASE_SAVE_DIR, exist_ok=True)

# List of last names to search for
LAST_NAMES = os.environ.get('LAST_NAMES', 'Pelosi').split(',')
LIST_NAMES = os.environ.get('LIST_NAMES', 'McCaul,Greene,Mullin').split(',')