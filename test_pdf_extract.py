import pdfplumber

pdf_path = "databasedata.pdf"  # Ensure this file is in your project folder

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"📄 Page {i+1} Content:\n{text}\n{'='*40}")
