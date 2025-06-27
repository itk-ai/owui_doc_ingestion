# Script written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import os

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
