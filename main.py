from flask import Flask, request, jsonify
import base64
import pdfkit

app = Flask(__name__)

def process_html_content(html_content, page_size='Letter'):
    """Converts an HTML content to base64 format.

    Args:
        html_content (str): The HTML content as a string.
        page_size (str): The size of the PDF page (default: 'Letter').

    Returns:
        str: The base64-encoded representation of the PDF file generated from the HTML.
    """
    pdf_file_path = "output.pdf"

    # Convert HTML to PDF
    options = {
        'page-size': page_size,
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
    }
    pdfkit.from_string(html_content, pdf_file_path, options=options)

    # Convert PDF to base64
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        encoded_data = base64.b64encode(pdf_data).decode("utf-8")  # Encode and decode for string output

    return encoded_data

@app.route('/convert_to_pdf', methods=['POST'])
def convert_to_pdf():
    try:
        html_content = request.data.decode("utf-8")
        if not html_content:
            raise ValueError("Missing HTML content in request body")

        page_size = request.args.get('page_size', 'Letter')

        base64_result = process_html_content(html_content, page_size)
        return jsonify({"base64_result": base64_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port="0.0.0.0")
