import PyPDF2

def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

    return text

# Example usage:
file_path = r'C:\Users\sawoo\OneDrive\Desktop\Girish Sawant - Resume - DA.pdf'
pdf_text = read_pdf(file_path)
print(pdf_text)
