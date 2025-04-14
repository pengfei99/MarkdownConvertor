import markdown
from weasyprint import HTML
# Get Pygments default style CSS
from pygments.formatters.html import  HtmlFormatter

def markdown_to_pdf(markdown_file_path, pdf_file_path=None):
    # If PDF filename not specified, use the same name as the markdown file but with .pdf extension
    if pdf_file_path is None:
        pdf_file_path = markdown_file_path.rsplit('.', 1)[0] + '.pdf'

    # Read a markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert the markdown file to HTML
    html_body = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite'])


    pygments_css = HtmlFormatter().get_style_defs('.codehilite')

    # Add some basic CSS for better formatting
    html_with_css = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            code {{ background-color: #f0f0f0; padding: 0.2em; }}
            pre {{ background-color: #f0f0f0; padding: 1em; }}
            blockquote {{ border-left: 3px solid #ccc; margin-left: 0; padding-left: 1em; }}
            
            /* Table styling with borders and separators */
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
                font-size: 0.9em;
            }}
            
            table, th, td {{
                border: 1px solid #ddd;
            }}
            
            th {{
                background-color: #f2f2f2;
                color: #333;
                font-weight: bold;
                text-align: left;
                padding: 10px;
            }}
            
            td {{
                padding: 8px;
                vertical-align: top;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            /* Add Pygments CSS for syntax highlighting */
            {pygments_css}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_with_css).write_pdf(pdf_file_path)

    return pdf_file_path