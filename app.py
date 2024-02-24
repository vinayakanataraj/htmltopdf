from flask import Flask, request, jsonify
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter
import base64
import pdfkit
import os

app = Flask(__name__)

# Retrieve the authentication key from an environment variable
auth_key = os.environ.get("AUTH_KEY")
auth_secret = os.environ.get("AUTH_SECRET")


def process_html_content(html_content, page_height, page_width, page_size='Letter', margin_top='0mm', margin_right='0mm', margin_bottom='0mm', margin_left='0mm'):
    """Converts an HTML content to base64 format.

    Args:
        html_content (str): The HTML content as a string.
        page_size (str): The size of the PDF page (default: 'Letter').
        margin_top (str): Top margin of the PDF page (default: '0mm').
        margin_right (str): Right margin of the PDF page (default: '0mm').
        margin_bottom (str): Bottom margin of the PDF page (default: '0mm').
        margin_left (str): Left margin of the PDF page (default: '0mm').

    Returns:
        str: The base64-encoded representation of the PDF file generated from the HTML.
    """
    pdf_file_path = "output.pdf"

    # Convert HTML to PDF
    options = {
        'page-size': page_size,
        'margin-top': margin_top,
        'margin-right': margin_right,
        'margin-bottom': margin_bottom,
        'margin-left': margin_left,
        'page-height': page_height,
        'page-width': page_width,
    }
    pdfkit.from_string(html_content, pdf_file_path, options=options)

    # Split PDF into pages and convert each page to base64
    encoded_pages = []
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        pdf_reader = PdfFileReader(BytesIO(pdf_data))
        for page_num in range(pdf_reader.numPages):
            output = PdfFileWriter()
            output.addPage(pdf_reader.getPage(page_num))
            with BytesIO() as output_pdf_bytes:
                output.write(output_pdf_bytes)
                encoded_pages.append(base64.b64encode(output_pdf_bytes.getvalue()).decode("utf-8"))

    return encoded_pages

@app.route('/convert_to_pdf', methods=['POST'])
def convert_to_pdf():
    try:
        # Check if the provided authentication key matches the predefined key
        provided_key = request.headers.get('auth_key')
        provided_secret = request.headers.get('auth_secret')
        if (provided_key != auth_key) or (provided_secret != auth_secret):
            # If authentication fails, return a 404 error
            return jsonify({"error": "Authentication failed"}), 401

        html_content = request.data.decode("utf-8")
        if not html_content:
            raise ValueError("Missing HTML content in request body")
        page_height = request.args.get('page_height')
        page_width = request.args.get('page_width')
        page_size = request.args.get('page_size', 'Letter')
        margin_top = request.args.get('margin_top', '0mm')
        margin_right = request.args.get('margin_right', '0mm')
        margin_bottom = request.args.get('margin_bottom', '0mm')
        margin_left = request.args.get('margin_left', '0mm')
        

        base64_result = process_html_content(html_content,page_height, page_width, page_size, margin_top, margin_right, margin_bottom, margin_left)
        return jsonify({"base64_result": base64_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)


# This web server is built on flask
