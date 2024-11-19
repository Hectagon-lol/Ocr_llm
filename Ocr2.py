import streamlit as st
import pytesseract
from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO

# Streamlit app
st.title("OCR with Bounding Box-based Text Placement in PDF")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Load the image
    image = Image.open(uploaded_file)

    # Perform OCR and get bounding boxes
    try:
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update based on installation
        ocr_data = pytesseract.image_to_boxes(image)

        # Generate the PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        # Get the image size
        img_width, img_height = image.size

        # Draw the text based on OCR bounding boxes
        for line in ocr_data.splitlines():
            char, x1, y1, x2, y2, _ = line.split()  # Box format: char, x1, y1, x2, y2
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

            # Convert coordinates to PDF's coordinate system
            x = x1
            y = img_height - y2  # Invert y-axis for PDF

            # Draw text
            pdf.drawString(x, y, char)

        # Save the PDF to buffer
        pdf.save()
        buffer.seek(0)

        # Allow the user to download the PDF
        st.success("OCR and bounding box-based text placement completed!")
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="output.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Example image size
img_width, img_height = 800, 600  # Replace with actual image size

# Example OCR bounding box coordinates
x0, y0, x1, y1 = 100, 500, 150, 550  # OCR coordinates (top-left, bottom-right)

# Create a PDF
pdf_path = "output.pdf"
pdf = canvas.Canvas(pdf_path, pagesize=letter)

# PDF page size (in points)
pdf_width, pdf_height = letter

# Map coordinates to PDF system
norm_x = x0 / img_width
norm_y = y0 / img_height

pdf_x = norm_x * pdf_width
pdf_y = (1 - norm_y) * pdf_height  # Flip Y-axis

# Draw the text
pdf.drawString(pdf_x, pdf_y, "Example Text")

# Save the PDF
pdf.save()
print(f"Text added to PDF at ({pdf_x}, {pdf_y}). Output saved to {pdf_path}.")
