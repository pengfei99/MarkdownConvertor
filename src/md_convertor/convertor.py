import markdown
from weasyprint import HTML

def markdown_to_pdf(markdown_file_path, pdf_file_path=None):
    # If PDF filename not specified, use the same name as the markdown file but with .pdf extension
    if pdf_file_path is None:
        pdf_file_path = markdown_file_path.rsplit('.', 1)[0] + '.pdf'

    # Read a markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert the markdown file to HTML
    html = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite'])

    # Add some basic CSS for better formatting
    html_with_css = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            code {{ background-color: #f0f0f0; padding: 0.2em; }}
            pre {{ background-color: #f0f0f0; padding: 1em; }}
            blockquote {{ border-left: 3px solid #ccc; margin-left: 0; padding-left: 1em; }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_with_css).write_pdf(pdf_file_path)

    return pdf_file_path