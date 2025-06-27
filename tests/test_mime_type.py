# Test written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import pytest
from owui_doc_ingestion.utils.mime_type import get_mime_type

def test_get_mime_type_pdf():
    pdf_path = "data/vielse/manually_extracted/Bekendtgørelse af lov om ægteskabs indgåelse og opløsning.pdf"
    mime_type = get_mime_type(pdf_path)
    assert mime_type == "application/pdf"

def test_get_mime_type_docx():
    docx_path = "data/vielse/manually_extracted/Hvem skal registrer en vielse og navneændring.docx"
    mime_type = get_mime_type(docx_path)
    assert mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def test_get_mime_type_nonexistent_file():
    nonexistent_file = "nonexistent_file.pdf"
    mime_type = get_mime_type(nonexistent_file)
    assert mime_type == "application/pdf"  # Should fall back to extension-based detection

def test_get_mime_type_invalid_extension():
    invalid_file = "test_file.xyz"
    mime_type = get_mime_type(invalid_file)
    assert mime_type is None  # Should return None for unrecognized extensions