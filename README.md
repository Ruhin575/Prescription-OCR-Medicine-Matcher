Prescription OCR & Medicine Matcher

Project Overview
This project is designed to improve the accessibility and accuracy of analyzing handwritten medical prescriptions in India. It leverages advanced Optical Character Recognition (OCR) and Natural Language Processing (NLP) techniques to extract and refine medicine names from prescription images, then matches these names against a trusted database. This solution is especially beneficial for visually impaired users and for ensuring that the handwritten prescriptions are interpreted correctly.

Key Features
• Handwritten Text Extraction:
Uses EasyOCR to convert prescription images into raw text, which is often more robust for handwritten text than other OCR engines.
• AI-based Text Refinement:
Utilizes the OpenAI ChatCompletion API (GPT‑3.5‑turbo) to process the OCR output and extract only the medicine names, formatted as a newline-separated list for easy parsing.
• Medicine Database Matching:
Loads a CSV file containing known medicine names and uses fuzzy matching (via rapidfuzz) to match and validate the extracted names against the database.
• Modular Pipeline:
The project is structured into clear steps (OCR, ChatGPT processing, database loading, and fuzzy matching) so that each component can be improved or replaced independently.

Installation
• Prerequisites
1. Python 3.7+
2. An OpenAI API key (obtain from OpenAI API Keys)
3. A CSV file named medicines.csv containing the medicine database. The file should have a header named "Drug Name" with one medicine name per row. 
• Required Python Packages
Install the necessary packages by running:
pip install openai easyocr pillow rapidfuzz

File Structure
• main.py:            Main pipeline script
• medicines.csv:      CSV database of medicine names
• README.md:            This file

Environment Setup
1. Clone this repository.
2. Create a new file in the project root named .env.
3. Add your API key to the file using the following format:
OPENAI_API_KEY="your_api_key_here"

How to Run
1. Prepare Your Prescription Image:
Ensure your image (e.g., prescription.jpg) is accessible from the project directory.
2. Run the Script:
python main.py
When prompted, enter the file path to your prescription image (ensure that any copied path does not include extra double quotes).
3. Review the Output:
The script will:
• Display the OCR-extracted text.
• Show the raw list of medicine names extracted by ChatGPT.
• Present the fuzzy-matched results, indicating which extracted names align with the entries in your medicine database along with a confidence score.

Limitations 
Currently, the database may not list all possible medicines or variations (including certain brand names and abbreviations used in India). As a result, some extracted medicine names may not find a match. Expanding and regularly updating the database is essential for improving matching accuracy.

Future Improvements
• Enhanced OCR: Use additional OCR services like Google cloud vision if the handwritten text is too noisy.
• Database Expansion: Update the medicines CSV with local Indian brand names and common abbreviations to improve matching accuracy.
• Integration with Medicine Ordering: Link this AI model to medicine ordering applications to automate the process so that visually impaired users don’t have to navigate inaccessible apps.
