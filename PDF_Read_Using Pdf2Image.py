import pdf2image
import io
import base64

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
    # Example usage:
file_path = r'C:\Users\sawoo\OneDrive\Desktop\Girish Sawant - Resume - DA.pdf'
with open(file_path, 'rb') as file:
    pdf_parts = input_pdf_setup(file)
print(pdf_parts)
