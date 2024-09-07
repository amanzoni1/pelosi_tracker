from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_driver_path = '/Users/andreamanzoni/Desktop/code/scripts/pelosi_tracker/chromedriver/chromedriver'

chrome_options = Options()
chrome_options.add_argument("--headless") 

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service)

driver.get('https://disclosures-clerk.house.gov/FinancialDisclosure')

search_button = driver.find_element(By.LINK_TEXT, 'Search')
search_button.click()

time.sleep(2)

last_name_input = driver.find_element(By.ID, 'LastName')
last_name_input.click()
last_name_input.send_keys('Pelosi')
# taylor greene -> sta copiando pelosi?

year_dropdown = driver.find_element(By.ID, 'FilingYear')
year_dropdown.click()
year_option = driver.find_element(By.XPATH, "//option[@value='2024']")
year_option.click()

submit_button = driver.find_element(By.XPATH, "//button[@aria-label='search button' and @title='Search']")
submit_button.click()

time.sleep(2)  
pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
for link in pdf_links:
    print(link.get_attribute('href'))


time.sleep(10)  

driver.quit()