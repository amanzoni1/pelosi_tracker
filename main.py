# main.py
import schedule
import time
from scraper import scrape_and_download_pdfs

def job():
    scrape_and_download_pdfs()

if __name__ == "__main__":
    schedule.every(30).seconds.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)