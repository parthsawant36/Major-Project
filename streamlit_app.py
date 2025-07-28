import streamlit as st
from PIL import Image
import fitz
import pytesseract
import io
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        full_text += f"\n--- Page {page_num} ---\n{text}"

        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(image)
            full_text += f"\n[Image OCR - Page {page_num} - Image {img_index + 1}]\n{ocr_text}"

    return full_text.lower()

def verify_pdf(text, required_phrases):
    return [phrase for phrase in required_phrases if phrase.lower() not in text]

# ---------- Streamlit UI ----------

st.title("PDF Authentication Feature")
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

required_phrases = st.text_area("Input Required Phrases ", "Lorem, Printing, Test")

if uploaded_pdf and required_phrases:
    if st.button("Authenticate PDF"):
        required_list = [p.strip() for p in required_phrases.split(',')]
        text = extract_text_from_pdf(uploaded_pdf)
        missing = verify_pdf(text, required_list)

        if not missing:
            st.success("✅ PDF is valid. All required phrases found.")
        else:
            st.error(f"❌ Missing phrases: {', '.join(missing)}")
