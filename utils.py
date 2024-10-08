# utils.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global constants
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_FROM_NAME = os.getenv('EMAIL_FROM_NAME')

MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.getenv('MAILJET_SECRET_KEY')
WELCOME_TEMPLATE_ID = os.getenv('MAILJET_WELCOME_TEMPLATE_ID')
UPDATE_TEMPLATE_ID = os.getenv('MAILJET_UPDATE_TEMPLATE_ID')

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')

# Base URL for scraping
BASE_URL = 'https://disclosures-clerk.house.gov/FinancialDisclosure'

# Directory to save PDFs
BASE_SAVE_DIR = os.path.join(os.getcwd(), 'savedPdf')

# List of last names to search for
LAST_NAMES = ['Pelosi', 'McCaul', 'Greene', 'Mullin']

# Ensure the base directory exists
os.makedirs(BASE_SAVE_DIR, exist_ok=True)