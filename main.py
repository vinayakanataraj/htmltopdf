from flask import Flask, request, jsonify
import base64
import pdfkit

app = Flask(__name__)

def process_html_content(html_content, page_size='Letter', margin_top='0mm', margin_right='0mm', margin_bottom='0mm', margin_left='0mm'):
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
        margin_top = request.args.get('margin_top', '0mm')
        margin_right = request.args.get('margin_right', '0mm')
        margin_bottom = request.args.get('margin_bottom', '0mm')
        margin_left = request.args.get('margin_left', '0mm')

        base64_result = process_html_content(html_content, page_size, margin_top, margin_right, margin_bottom, margin_left)
        return jsonify({"base64_result": base64_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
