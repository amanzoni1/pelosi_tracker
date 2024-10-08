import os
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

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
                        "If the text is incoherent, provide the biggest move by amount and any other relevant insights or whatever you can get:\n\n"
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

# Example usage
if __name__ == "__main__":
    pdf_file_path = './savedPdf/Pelosi/20024542.pdf'
    result = analyze_pdf(pdf_file_path)
    print("Analysis Result:\n", result)