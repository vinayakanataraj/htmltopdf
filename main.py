import pdfkit
import base64

def convert_pdf_to_base64(pdf_file_path):
    """Converts a PDF file to base64 format, suitable for printer input.

    Args:
        pdf_file_path (str): The path to the PDF file.

    Returns:
        str: The base64-encoded representation of the PDF file.
    """

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        encoded_data = base64.b64encode(pdf_data).decode("utf-8")  # Encode and decode for string output

    return encoded_data

def convert_html_to_pdf(html_file, pdf_file):
    options = {
        'page-size': 'Letter',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
    }
    pdfkit.from_file(html_file, pdf_file, options=options)

# Example usage
html_file_path = 'index.html'
pdf_file_path = 'output.pdf'

convert_html_to_pdf(html_file_path, pdf_file_path)
