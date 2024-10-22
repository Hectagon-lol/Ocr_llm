# import streamlit as st
# from PIL import Image
# import pytesseract
# from pdf2image import convert_from_path
# import os

# # Set the path to the Tesseract executable for Windows users
# pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

# # Initialize an empty string to hold the combined OCR text
# combined_text = ""

# # Convert PDF to images
# images = convert_from_path(r"C:\Users\abhij\Downloads\TCS CodeVita Season 11 Certificate - abhijit_tk.pdf", 500, poppler_path=r'./poppler-24.08.0/Library/bin')

# # Loop over all images and apply OCR
# for i, image in enumerate(images):
#     # Save image as PNG file
#     fname = 'image' + str(i) + '.png'
#     image.save(fname, "PNG")
    
#     # Open the image file
#     img = Image.open(fname)
    
#     # Perform OCR on the image
#     ocr_text = pytesseract.image_to_string(img)
    
#     # Add OCR text to the combined string
#     combined_text += ocr_text + "\n"

# # Display the extracted text using Streamlit
# st.write(combined_text)


import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import io

# Set the path to the Tesseract executable for Windows users
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

# Title of the app
st.title("PDF and Image OCR App")

# File uploader for PDFs and images
uploaded_file = st.file_uploader("Upload PDF or Image (JPG/PNG)", type=["pdf", "jpg", "jpeg", "png"])

# Initialize an empty string to hold the combined OCR text
combined_text = ""

# Check if a file has been uploaded
if uploaded_file is not None:
    # If the uploaded file is a PDF
    if uploaded_file.type == "application/pdf":
        # Convert PDF to images
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Convert the PDF into images using pdf2image
        images = convert_from_path("temp.pdf", 500, poppler_path=r'./poppler-24.08.0/Library/bin')

        # Loop over all images and apply OCR
        for i, image in enumerate(images):
            # Perform OCR on the image
            ocr_text = pytesseract.image_to_string(image)

            # Add OCR text to the combined string
            combined_text += ocr_text + "\n"

    # If the uploaded file is an image
    elif uploaded_file.type in ["image/jpeg", "image/png"]:
        # Read the image file
        img = Image.open(uploaded_file)

        # Perform OCR on the image
        ocr_text = pytesseract.image_to_string(img)

        # Add OCR text to the combined string
        combined_text += ocr_text + "\n"

    # Display the extracted text
    st.subheader("Extracted Text")
    st.write(combined_text)
