import mammoth
import argparse

def convert_docx_to_html(input_filename, output_filename):
    """Converts a file from .docx to .html.

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


if __name__ == '__main__':
    """
    Converts a file from .docx to .html.

    positional arguments:
        input-file-name   The input path to the file that is being converted from .docx to .html
        output-file-name  The output path to the file that is being converted from .docx to .html

    """

    parser = argparse.ArgumentParser(description='Converts a file from .docx to .html.')

    parser.add_argument('InFile',
                        metavar='input-file-name',
                        type=str,
                        help='The input path to the file that is being converted from .docx to .html')

    parser.add_argument('OutFile',
                        metavar='output-file-name',
                        type=str,
                        help='The output path to the file that is being converted from .docx to .html')

    args = parser.parse_args()

    input_filename = args.InFile
    output_filename = args.OutFile

    convert_docx_to_html(input_filename, output_filename)