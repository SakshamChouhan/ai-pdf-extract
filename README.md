# ai-pdf-extract

**ai-pdf-extract** is a Python-based web application that extracts and processes key information (such as Name, Phone Number, and Address) from PDF files. Using advanced NLP (Natural Language Processing) techniques with SpaCy and text extraction from PDFs via pdfplumber, this app allows users to upload PDFs and automatically extract structured data.

## Features:
- **Extracts Text**: Uses `pdfplumber` to extract raw text from PDF documents.
- **Named Entity Recognition**: Utilizes SpaCy's pre-trained models to detect names, phone numbers, and addresses.
- **API Integration**: Exposes a RESTful API endpoint to handle file uploads and return the extracted details in JSON format.

## Requirements

Before running the project, make sure you have the following dependencies installed:

- **Python 3.x**
- `Flask`
- `Flask-Cors`
- `spaCy`
- `pdfplumber`

You can install the required dependencies with:

```bash
pip install -r requirements.txt
```

You will also need to download the **SpaCy language model**:

```bash
python -m spacy download en_core_web_lg
```

## Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-pdf-extract.git
   cd ai-pdf-extract
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```

4. The app will run on `http://127.0.0.1:5000/`.

## Usage

To extract information from a PDF, send a POST request to the `/upload` endpoint with the PDF file attached:

**Request**:
```bash
POST http://127.0.0.1:5000/upload
Content-Type: multipart/form-data
```

**Body**: Attach the PDF file using the `file` field.

**Response**:
```json
{
  "Name": "John Doe",
  "Phone": "1234567890",
  "Address": "1234 Main St, Springfield, IL"
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---