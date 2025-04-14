from md_convertor.convertor import markdown_to_pdf

def test_markdown_to_pdf():
    markdown_file_path = '../data/sample.md'
    pdf_path = markdown_to_pdf(markdown_file_path)
    print(f"PDF created: {pdf_path}")
