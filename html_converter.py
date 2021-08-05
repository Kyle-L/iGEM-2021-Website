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


if __name__ == '__main__':
    """
    Converts a file from .doc, .docx, or .md to .html.

    positional arguments:
        input-file-name   The input path to the file that is being converted from .doc, .docx, or .md to .html
        output-file-name  The output path to the file that is being converted from .doc, .docx, or .md to .html

    """

    parser = argparse.ArgumentParser(description='Converts a file from .doc, .docx, or .md to .html.')

    parser.add_argument('InFile',
                        metavar='input-file-name',
                        type=str,
                        help='The input path to the file that is being converted from .doc, .docx, or .md to .html')

    parser.add_argument('OutFile',
                        metavar='output-file-name',
                        type=str,
                        help='The output path to the file that is being converted from .doc, .docx, or .md to .html')

    args = parser.parse_args()

    input_filename = args.InFile
    output_filename = args.OutFile

    if input_filename.endswith('.docx') or input_filename.endswith('.doc'):
        convert_docx_to_html(input_filename, output_filename)

    elif input_filename.endswith('.md'):
        convert_md_to_html(input_filename, output_filename)

    else:
        print('Invalid input! Please provide a input-file-name that ends in one of the following: [.docx, .doc, .md]')
