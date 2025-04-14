from convertor import markdown_to_pdf
import sys





if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        pdf_path = markdown_to_pdf(input_file, output_file)
        print(f"PDF created: {pdf_path}")
    else:
        print("Usage: python script.py input.md [output.pdf]")