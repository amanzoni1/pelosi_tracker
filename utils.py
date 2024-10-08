import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global constants
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')
MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.getenv('MAILJET_SECRET_KEY')
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_FROM_NAME = os.getenv('EMAIL_FROM_NAME')

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH = '/Users/andreamanzoni/Desktop/code/scripts/pelosi_tracker/chromedriver/chromedriver'

# Base URL for scraping
BASE_URL = 'https://disclosures-clerk.house.gov/FinancialDisclosure'

# Directory to save PDFs
BASE_SAVE_DIR = os.path.join(os.getcwd(), 'savedPdf')

# List of last names to search for
LAST_NAMES = ['Pelosi', 'McCaul', 'Greene', 'Mullin']

# Ensure the base directory exists
os.makedirs(BASE_SAVE_DIR, exist_ok=True)