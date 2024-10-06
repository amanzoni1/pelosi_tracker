import os
import time
import requests
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Path to the ChromeDriver executable
chrome_driver_path = '/Users/andreamanzoni/Desktop/code/scripts/pelosi_tracker/chromedriver/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") 

# Set up the ChromeDriver service
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# List of last names to search for
last_names = ['Pelosi', 'McCaul', 'Greene', 'Mullin']
waiting = ['Crenshaw']

# Base URL
base_url = 'https://disclosures-clerk.house.gov/FinancialDisclosure'

# Directory to save PDFs
base_save_dir = os.path.join(os.getcwd(), 'savedPdf')

# Create the base directory if it doesn't exist
if not os.path.exists(base_save_dir):
    os.makedirs(base_save_dir)

# Function to read PDF and extract text
def extract_text_from_pdf(pdf_file):
    # First, try extracting text with pdfplumber
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
            # Return text if extraction was successful
            if text.strip():
                return text.strip()
    except Exception as e:
        print(f"Error reading the PDF file with pdfplumber: {e}")

    # If pdfplumber fails or returns no text, use OCR
    try:
        pages = convert_from_path(pdf_file)
        text = ''
        for page in pages:
            text += pytesseract.image_to_string(page)  # Apply OCR
        return text.strip()  # Return stripped text from OCR
    except Exception as e:
        print(f"Error reading the PDF file with OCR: {e}")
        return None

# Function to interact with GPT-4 API using chat completions
def send_pdf_text_to_gpt4(pdf_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Please summarize the stocks mentioned in the following text. "
                        "Format the summary as a table with the following columns: "
                        "Stock Name, Ticker, Action Taken, Quantity of Shares, and Amount of Transaction. "
                        "If the text is incoherent, provide the biggest move by amount and any other relevant insights:\n\n"
                        f"{pdf_text}"
                    )
                }
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error interacting with the OpenAI API: {e}")
        return None

# Main function to handle PDF file and call GPT-4 API
def analyze_pdf(pdf_file):
    pdf_text = extract_text_from_pdf(pdf_file)
    if pdf_text:
        analysis = send_pdf_text_to_gpt4(pdf_text)
        return analysis
    return "No text extracted from the PDF."

# Loop through each last name
for last_name in last_names:
    driver.get(base_url)

    # Click the "Search" button or link
    try:
        search_button = driver.find_element(By.LINK_TEXT, 'Search')
        search_button.click()
    except Exception as e:
        print(f"Failed to find or click the Search button for {last_name}: {e}")
        continue

    time.sleep(2)  # Wait for the element to load

    # Enter text into the "LastName" input field
    try:
        last_name_input = driver.find_element(By.ID, 'LastName')
        last_name_input.clear()
        last_name_input.send_keys(last_name)
    except Exception as e:
        print(f"Failed to enter last name {last_name}: {e}")
        continue

    # Select the "FilingYear" from the dropdown (2024)
    try:
        year_dropdown = driver.find_element(By.ID, 'FilingYear')
        year_dropdown.click()
        year_option = driver.find_element(By.XPATH, "//option[@value='2024']")
        year_option.click()
    except Exception as e:
        print(f"Failed to select Filing Year for {last_name}: {e}")
        continue

    # Click the "Search" button to submit the form
    try:
        submit_button = driver.find_element(By.XPATH, "//button[@aria-label='search button' and @title='Search']")
        submit_button.click()
    except Exception as e:
        print(f"Failed to click Search button for {last_name}: {e}")
        continue

    time.sleep(5)  # Wait for the search results to load

    # Initialize lists for tracking
    new_pdfs = []
    failed_pdfs = []

    # Check if there are any results
    try:
        # Locate the search results table
        results_table = driver.find_element(By.ID, 'search-result')
        # Extract PDF links only from the search results section
        pdf_links = results_table.find_elements(By.XPATH, ".//a[contains(@href, '.pdf')]")

        if not pdf_links:
            print(f"No PDFs found for {last_name}.")
            continue

        # Create a directory for the last name
        last_name_dir = os.path.join(base_save_dir, last_name)
        os.makedirs(last_name_dir, exist_ok=True)

        # Download each PDF if it doesn't already exist
        for link in pdf_links:
            pdf_url = link.get_attribute('href')
            pdf_name = os.path.basename(pdf_url)
            pdf_path = os.path.join(last_name_dir, pdf_name)

            if os.path.exists(pdf_path):
                continue

            # Construct the full URL
            full_pdf_url = urljoin(base_url, pdf_url)
            print(f"Attempting to download: {full_pdf_url}")

            try:
                response = requests.get(full_pdf_url)
                if response.status_code == 200:
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    new_pdfs.append(pdf_name)
                    
                    # Analyze the newly downloaded PDF
                    analysis_result = analyze_pdf(pdf_path)
                    print(f"Analysis Result for {pdf_name}:\n", analysis_result)

                else:
                    print(f"Failed to download {pdf_name}: HTTP {response.status_code}")
                    failed_pdfs.append(pdf_name)
            except Exception as e:
                print(f"Error downloading {pdf_name}: {e}")
                failed_pdfs.append(pdf_name)

    except Exception as e:
        print(f"No results found for {last_name} or an error occurred: {e}")
        continue

    # Log the results
    if new_pdfs:
        print(f"New PDFs downloaded for {last_name}:")
        for pdf in new_pdfs:
            print(f"  - {pdf}")
    else:
        print(f"Nothing new for {last_name}.")

    if failed_pdfs:
        print(f"Failed to download the following PDFs for {last_name}:")
        for pdf in failed_pdfs:
            print(f"  - {pdf}")

print("-" * 40)

# Close the browser
driver.quit()