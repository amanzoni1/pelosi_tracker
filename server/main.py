# server/main.py

import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

import schedule
import time
from scraper import scrape_and_download_pdfs

def job():
    scrape_and_download_pdfs()

if __name__ == "__main__":
    schedule.every(20).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)