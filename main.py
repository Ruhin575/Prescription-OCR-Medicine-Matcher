import os
from dotenv import load_dotenv
import openai
import easyocr
from PIL import Image
import csv
from rapidfuzz import process, fuzz

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file")

def ocr_image(image_path):
    """
    Extracts text from an image using EasyOCR.
    EasyOCR is often more robust for handwritten text.
    """
    reader = easyocr.Reader(['en'])  # specify languages; add more if needed (e.g., 'hi' for Hindi)
    # detail=0 returns only the recognized text strings
    results = reader.readtext(image_path, detail=0)
    # Join all text segments into one string
    text = " ".join(results)
    return text

def get_chat_response(ocr_text):
    """
    Sends the OCR text to ChatGPT and gets a refined output.
    The prompt instructs the model to extract only the medicine names
    from the OCR text and output them as a newline-separated list.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in reading handwritten prescriptions. "
                "Extract only the medicine names from the following OCR text. "
                "Output them as a newline-separated list. Do not include dosages or commentary."
            )
        },
        {
            "role": "user",
            "content": f"Extract medicine names from the following OCR result:\n\n{ocr_text}"
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]

def load_medicine_database(csv_path="medicines.csv"):
    """
    Loads medicine names from a CSV file.
    Assumes the CSV has a header "Drug Name" and each subsequent row contains one medicine name.
    """
    medicines = []
    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            medicine = row.get("Drug Name", "").strip()
            if medicine:
                medicines.append(medicine)
    return medicines

def match_medicines(extracted_names, medicine_db, threshold=80):
    """
    Uses fuzzy matching to map each extracted medicine name to the closest match
    in the medicine database. Returns a list of tuples: (extracted, best_match, score).
    """
    matched = []
    for name in extracted_names:
        best = process.extractOne(name, medicine_db, scorer=fuzz.token_sort_ratio)
        if best and best[1] >= threshold:
            matched.append((name, best[0], best[1]))
        else:
            matched.append((name, None, 0))
    return matched

def main():
    # Step 1: Get the OCR text from the prescription image using EasyOCR
    image_path = input("Enter the image file path (e.g., prescription.jpg): ")
    ocr_text = ocr_image(image_path)
    print("\nOCR Extracted Text:")
    print(ocr_text)
    
    # Step 2: Use ChatGPT to extract medicine names (newline-separated)
    chat_response = get_chat_response(ocr_text)
    print("\nExtracted Medicine Names (Raw):")
    print(chat_response)
    
    # Step 3: Parse the newline-separated medicine names from ChatGPT's output
    extracted_names = [name.strip() for name in chat_response.splitlines() if name.strip()]
    
    # Step 4: Load the medicine database from a CSV file
    medicine_db = load_medicine_database("medicines.csv")
    
    # Step 5: Fuzzy match the extracted names against the database
    matches = match_medicines(extracted_names, medicine_db)
    
    print("\nMatched Medicine Names:")
    for orig, match, score in matches:
        if match:
            print(f"Extracted: '{orig}' --> Matched: '{match}' (score: {score})")
        else:
            print(f"Extracted: '{orig}' --> No match found")
    
if __name__ == "__main__":
    main()