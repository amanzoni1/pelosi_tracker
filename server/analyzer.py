# server/analyzer.py

import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from openai import OpenAI
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

from shared.utils import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_text_from_pdf(pdf_file):
    # First, try extracting text with pdfplumber
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
            if text.strip():
                return text.strip()
    except Exception as e:
        print(f"Error reading the PDF file with pdfplumber: {e}")
    # If pdfplumber fails, use OCR
    try:
        pages = convert_from_path(pdf_file)
        text = ''
        for page in pages:
            text += pytesseract.image_to_string(page)
        return text.strip()
    except Exception as e:
        print(f"Error reading the PDF file with OCR: {e}")
        return None

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

def analyze_pdf(pdf_file, last_name):
    pdf_text = extract_text_from_pdf(pdf_file)
    if pdf_text:
        analysis_result = send_pdf_text_to_gpt4(pdf_text)
        if analysis_result:
            return analysis_result
    return None