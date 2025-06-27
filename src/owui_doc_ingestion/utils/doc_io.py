# Script written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import os
import os, zipfile, xml.dom.minidom, sys
from docx import Document
from pypdf import PdfReader


def save_docs_to_md(docs, base_filepath, out_folder=None):
    """
    Save documents to markdown files.

    Args:
        docs: List of documents with page_content
        base_filepath: Original input file path to derive output filename
        out_folder: Optional output folder path
    """
    base_name = os.path.splitext(os.path.basename(base_filepath))[0]

    # Use output folder if specified, otherwise use input file's directory
    if out_folder:
        os.makedirs(out_folder, exist_ok=True)
        output_dir = out_folder
    else:
        output_dir = os.path.dirname(base_filepath)

    # Handle single or multiple documents
    for i, doc in enumerate(docs):
        # For single doc, use base name; for multiple docs, append number
        if len(docs) == 1:
            output_filename = f"{base_name}.md"
        else:
            output_filename = f"{base_name}_{i + 1}.md"

        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc.page_content)


def get_page_count(file_path:str, mime_type:str) -> int | None:
    """Get page count based on file type using appropriate library."""
    try:
        if mime_type == 'application/pdf':
            with open(file_path, 'rb') as file:
                pdf = PdfReader(file)
                return len(pdf.pages)
        elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                           'application/msword']:
            # Method from https://github.com/muhammadmoazzam/word-page-count/blob/master/word-page.py
            doc = zipfile.ZipFile(file_path)
            dxml = doc.read('docProps/app.xml')
            ugly_xml = xml.dom.minidom.parseString(dxml)
            page_nb = int(ugly_xml.getElementsByTagName('Pages')[0].childNodes[0].nodeValue)

            return page_nb
        return None
    except Exception as e:
        print(f"Error getting page count for {file_path}: {str(e)}")
        return None
