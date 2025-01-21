import re
import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import sys
import subprocess

# Ensure SpaCy model is installed
try:
    spacy.load('en_core_web_lg')
except OSError:
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_lg'])
    nlp = spacy.load('en_core_web_lg')
                     
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

nlp = spacy.load('en_core_web_lg') 

def extract_text_from_pdf(file):
    """Extract text from PDF using pdfplumber."""
    with pdfplumber.open(file) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text

def extract_details(text):
    """Extract name, phone number, and address using SpaCy and Regex."""
    details = {"Name": None, "Phone": None, "Address": None}

    # Step 1: Named Entity Recognition using SpaCy
    doc = nlp(text)


    # Step 2: Extract Name with SpaCy NER
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            details["Name"] = ent.text

    # Step 3: Manually Combine phone number parts from CARDINAL entities
    phone_parts = []
    for ent in doc.ents:
        if ent.label_ == "CARDINAL":
            if re.match(r"^\+?\d+$", ent.text):
                phone_parts.append(ent.text)
    if phone_parts:
        details["Phone"] = ''.join(phone_parts)  # Combine phone number parts

    # Step 4: Combine address-related entities (GPE, CARDINAL) into address
    address_entities = [ent.text for ent in doc.ents if ent.label_ in ["GPE"]]
    if address_entities:
        details["Address"] = " ".join(address_entities)

    # Step 5: Use Regex for address detection (optional)
    address_pattern = r"\d{1,5}\s[A-Za-z0-9\s]+(?:[A-Za-z]+\s?)+(?:[A-Za-z]+\s?)+,\s?[A-Za-z\s]+,\s?[A-Za-z\s]+,\s?\d{5,}"
    address_match = re.search(address_pattern, text)
    if address_match and not details["Address"]:
        details["Address"] = address_match.group()
    

    return details

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and extract details."""
    file = request.files['file']
    if file:
        text = extract_text_from_pdf(file)
        details = extract_details(text)
        return jsonify(details)
    return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)
