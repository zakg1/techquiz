import fitz  # PyMuPDF

def extract_text_from_pdf(path):
    text = ""
    pdf = fitz.open(path)

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text
