import pytesseract
from PIL import Image
from reportlab.pdfgen import canvas

# Specify the path to tesseract executable (adjust based on your installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image
image_path = "input_image.jpg"  # Replace with your image path
image = Image.open(image_path)

# Perform OCR and get bounding boxes
ocr_data = pytesseract.image_to_boxes(image)

# Create a PDF and add text at positions
pdf_path = "output.pdf"
pdf = canvas.Canvas(pdf_path)

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

# Save the PDF
pdf.save()

print(f"OCR and bounding box-based text placement completed. Output saved to {pdf_path}.")
