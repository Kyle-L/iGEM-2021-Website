import mammoth
import markdown
import argparse


def convert_docx_to_html(input_filename, output_filename):
    """Converts a file from .doc, .docx, or .md to .html.

    Args:
        input_filename (str): The file path of the input .docx file.
        output_filename (str): The file path of the outputted .html file.
    """    

    with open(input_filename, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

        # Encodes and decodes the html to remove unicode blocks.
        html = html.encode("ascii", "ignore").decode()

        with open(output_filename, 'w') as text_file:
            text_file.write(html)


def convert_md_to_html(input_filename, output_filename):
    """Converts a file from .doc, .docx, or .md to .html.

    Args:
        input_filename (str): The file path of the input .docx file.
        output_filename (str): The file path of the outputted .html file.
    """    

    with open(input_filename, "rb") as md_file:
        markdown.markdownFromFile(
            input=md_file,
            output=output_filename,
            encoding='utf8',
        )


def auto_convert_to_html(input_filename, output_filename):
    """Auto converts .docx, .doc, or .md to html.

    Args:
        input_filename (str): The file path of the input .docx, .doc, or .md file.
        output_filename (str): The file path of the outputted .docx, .doc, or .md file.
    """    

    if input_filename.endswith('.docx') or input_filename.endswith('.doc'):
        convert_docx_to_html(input_filename, output_filename)

    elif input_filename.endswith('.md'):
        convert_md_to_html(input_filename, output_filename)

    else:
        print('Invalid input! Please provide a input-file-name that ends in one of the following: [.docx, .doc, .md]')
