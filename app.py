from flask import Flask, request, jsonify
import pdfkit
import base64
import os
import json
from barcode import Code39, writer


app = Flask(__name__)

# Retrieve the authentication key and secret from environment variables
AUTHORIZED_KEY = os.environ.get("AUTH_KEY")
AUTHORIZED_SECRET = os.environ.get("AUTH_SECRET")

def is_authorized(request):
    provided_key = request.headers.get('auth_key')
    provided_secret = request.headers.get('auth_secret')
    return provided_key == AUTHORIZED_KEY and provided_secret == AUTHORIZED_SECRET

def html_to_pdf_base64(html_input, options=None):
    options = options or {}
    pdf_bytes = pdfkit.from_string(html_input, False, options=options)
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return pdf_base64

def generate_barcode_and_html(data):
   """
   Generates a unique barcode number, creates a Code 39 barcode image,
   generates an HTML table with the barcode embedded, and returns the
   barcode image filename and the HTML table content.

   Args:
       data: A dictionary containing the JSON data.

   Returns:
       A tuple containing the barcode image filename (string) and the HTML table content (string).
   """

   # Optimize for speed by avoiding unnecessary sorting and hashing
   barcode_key = json.dumps(data)  # Use data as-is for key

   # Generate unique ID and create barcode
   unique_id = data["unitID"]
   barcode = Code39(unique_id, writer=writer.ImageWriter)
   barcode_filename = f"barcode"
   barcode.save(barcode_filename)

   # Generate HTML table directly, avoiding separate function call
   size = data["unitSize"]
   od = data["unitOD"]
   weight = "{:.3f}".format(data["unitWeight"])
   brand = data["unitBrand"]
   mrp = "{:.2f}".format(1200*(float(data["unitWeight"])))

   table_html = f"""
   <table border="1" style="border-collapse: collapse;">
       <tr>
           <td colspan="2"><img src="{barcode_filename}.svg" alt="Barcode"></td>
       </tr>
       <tr>
           <th>Size (mm)</th>
           <th>OD (mm)</th>
       </tr>
       <tr>
           <td>{size}</td>
           <td>{od}</td>
       </tr>
       <tr>
           <th>Weight (kg)</th>
           <th>Brand</th>
       </tr>
       <tr>
           <td>{weight}</td>
           <td>{brand}</td>
       </tr>
       <tr>
           <td colspan="2"><b>MRP: ₹{mrp}</b></td>
       </tr>
   </table>
   """

   return barcode_filename, table_html


@app.route('/convert_to_pdf', methods=['POST'])
def convert_to_pdf():
    try:
        # Check if the provided authentication key matches the predefined key
        if not is_authorized(request):
            return jsonify({"error": "Authentication failed"}), 401

        html_input = request.get_data(as_text=True)

        pdf_options = {
            'page-size': request.args.get('page_size', 'A4'),
            'orientation': request.args.get('orientation', 'Portrait'),
            'margin-top': request.args.get('margin_top', '0mm'),
            'margin-right': request.args.get('margin_right', '0mm'),
            'margin-bottom': request.args.get('margin_bottom', '0mm'),
            'margin-left': request.args.get('margin_left', '0mm'),
        }

        pdf_bytes = pdfkit.from_string(html_input, False, options=pdf_options)

        # Save the entire PDF to 'output.pdf'
        with open('output.pdf', 'wb') as output_file:
            output_file.write(pdf_bytes)

        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        return jsonify({'base64': pdf_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_barcode', methods=['POST'])
def generate_barcode():
    try:
        if not is_authorized(request):
            return jsonify({"error": "Authentication failed"}), 401
        
        data = request.get_data(as_text=True)
        data = json.dumps(data)
        barcode_filename, table_html = generate_barcode_and_html(data) 

        html_input = table_html

        pdf_options = {
            'page-size': request.args.get('page_size', 'A4'),
            'orientation': request.args.get('orientation', 'Portrait'),
            'margin-top': request.args.get('margin_top', '0mm'),
            'margin-right': request.args.get('margin_right', '0mm'),
            'margin-bottom': request.args.get('margin_bottom', '0mm'),
            'margin-left': request.args.get('margin_left', '0mm'),
        }

        pdf_bytes = pdfkit.from_string(html_input, False, options=pdf_options)

        # Save the entire PDF to 'output.pdf'
        with open('output.pdf', 'wb') as output_file:
            output_file.write(pdf_bytes)

        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        return jsonify({'base64': pdf_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
