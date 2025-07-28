from PIL import Image
import fitz 
import pytesseract
import io
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


pdfs = "Lorem_ipsum.pdf"
def extract_text_from_pdf(pdfs) :
    
    doc = fitz.open(pdfs)
    full_text = ""
    
    for page_num , page in  enumerate(doc , start = 1) :
        text = page.get_text()
        print(f"[INFO] Page {page_num} scanned.")
        full_text += f"\n--- Page {page_num} ---\n{text}" 
        
        images = page.get_images(full=True)
        print(f"[INFO] Page {page_num} contains {len(images)} image(s).")
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            
            ocr_text = pytesseract.image_to_string(image)
            print(f"[OCR] Text from image {img_index + 1} on page {page_num}: {ocr_text.strip()}")
            full_text += f"\n[Image OCR - Page {page_num} - Image {img_index + 1}]\n{ocr_text}"
            
        

        
    return full_text.lower()

def verify_pdf(full_text , required_phrases) :
    missing_phrase = []
    for phrase in required_phrases :
        if phrase.lower() not in full_text :
            missing_phrase.append(phrase)
            
    return missing_phrase
    
def authenticate_pdf(pdfs , required_phrases) :
    
     
    text = extract_text_from_pdf(pdfs)
    missing = verify_pdf(text , required_phrases)
     
    if not missing:
        print(" PDF is valid. All required phrases found.")
        
    else:
        print(" PDF is invalid. Missing phrases:")
        for phrase in missing:
            print(f" - {phrase}")
            
            

if __name__ == "__main__":
    
    pdf_file = "Lorem_ipsum.pdf"  

    
    required_text = [
        "Lorem",
        "Printing",
        "Test"
    ]

    
    authenticate_pdf(pdf_file, required_text)

    
    
    