import mammoth
import markdown
import argparse

def convert_docx_to_html(input_filename):
    """Converts a file from .doc or .docx to .html and returns it as a 'utf-8' string.

    Args:
        input_filename (str): The file path of the input .doc or .docx file.
    """    

    with open(input_filename, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value


def convert_and_save_docx_to_html(input_filename, output_filename):
    """Converts a file from .doc or .docx to .html and writes it to 'utf-8' file.

    Args:
        input_filename (str): The file path of the input .docx file.
        output_filename (str): The file path of the outputted .html file.
    """    

    html = convert_docx_to_html(input_filename)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

def convert_md_to_html(input_filename):
    """Converts a file from .md to .html and returns it as a 'utf-8' string.

    Args:
        input_filename (str): The file path of the input .docx file.
    """    

    with open(input_filename, 'r') as file:
        text = file.read()
        html = markdown.markdown(text, extensions=['tables', 'meta'])
        return html

def convert_and_save_md_to_html(input_filename, output_filename):
    """Converts a file from .md to .html and writes it to 'utf-8' file.

    Args:
        input_filename (str): The file path of the input .md file.
        output_filename (str): The file path of the outputted .html file.
    """    

    html = convert_docx_to_html(input_filename)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)


def convert_docx_to_md(input_filename):
    """Converts a file from .doc or .docx to .md and returns it as a 'utf-8' string.

    Args:
        input_filename (str): The file path of the input .docx file.
    """    

    with open(input_filename, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        return result.value

def convert_and_save_docx_to_md(input_filename, output_filename):
    """Converts a file from .doc or .docx to .md and writes it to 'utf-8' file.

    Args:
        input_filename (str): The file path of the input .docx file.
        output_filename (str): The file path of the outputted .md file.
    """    

    html = convert_docx_to_md(input_filename)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

def auto_convert(input_filename, output_file):
    """Auto converts .docx, .doc, or .md to .html or .md.

    Args:
        input_filename (str): The file path of the input .docx, .doc, or .md file.
    """    

    if (input_filename.endswith('.docx') or input_filename.endswith('.doc')) and output_file.endswith('.html'):
        convert_and_save_docx_to_html(input_filename, output_file)

    elif (input_filename.endswith('.docx') or input_filename.endswith('.doc')) and output_file.endswith('.md'):
        convert_and_save_docx_to_md(input_filename, output_file)

    elif input_filename.endswith('.md') and output_file.endswith('.html'):
        convert_and_save_md_to_html(input_filename, output_file)

    else:
        print('Invalid input! Please provide a input-file-name that ends in one of the following: [.docx, .doc, .md]')
