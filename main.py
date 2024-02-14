import pdfkit

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
