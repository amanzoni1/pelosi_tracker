# server/main.py

import sys
import os
import schedule
import time
import logging
from scraper import scrape_and_download_pdfs

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)


def job():
    try:
        logger.info("Starting scrape job...")
        scrape_and_download_pdfs()
        logger.info("Scrape job completed successfully.")
    except Exception as e:
        logger.exception("An error occurred during the scrape job:")
     
if __name__ == "__main__":
    schedule.every(20).seconds.do(job)
    logger.info("Scraper worker started. Running jobs every 20 seconds.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scraper worker stopped manually.")
    except Exception as e:
        logger.exception("Scraper worker encountered an unexpected error:")
        sys.exit(1)