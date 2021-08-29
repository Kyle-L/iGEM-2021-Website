import mammoth
import markdown
import argparse

def convert_docx_to_html(input_filename):
    """Converts a file from .doc, .docx, or .md to .html.

    Args:
        input_filename (str): The file path of the input .docx file.
    """    

    with open(input_filename, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        return html


def convert_md_to_html(input_filename):
    """Converts a file from .doc, .docx, or .md to .html.

    Args:
        input_filename (str): The file path of the input .docx file.
    """    

    with open(input_filename, 'r') as file:
        text = file.read()
        html = markdown.markdown(text)
        return html

def auto_convert_to_html(input_filename):
    """Auto converts .docx, .doc, or .md to html.

    Args:
        input_filename (str): The file path of the input .docx, .doc, or .md file.
    """    

    if input_filename.endswith('.docx') or input_filename.endswith('.doc'):
        return convert_docx_to_html(input_filename)

    elif input_filename.endswith('.md'):
        return convert_md_to_html(input_filename)

    else:
        print('Invalid input! Please provide a input-file-name that ends in one of the following: [.docx, .doc, .md]')
