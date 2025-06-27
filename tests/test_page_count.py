import pytest
from owui_doc_ingestion.utils.doc_io import get_page_count

def test_get_page_count():
    # Test PDF file with 15 pages
    pdf_path = "data/vielse/manually_extracted/Bekendtgørelse af lov om ægteskabs indgåelse og opløsning.pdf"
    pdf_result = get_page_count(pdf_path, "application/pdf")
    assert pdf_result == 15, f"Expected 15 pages for PDF, got {pdf_result}"

    # Test DOCX file with 2 pages
    docx_path = "data/vielse/manually_extracted/Hvem skal registrer en vielse og navneændring.docx"
    docx_result = get_page_count(docx_path, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert docx_result == 2, f"Expected 2 pages for DOCX, got {docx_result}"

def test_get_page_count_invalid_file():
    # Test with non-existent file
    result = get_page_count("nonexistent.pdf", "application/pdf")
    assert result is None, "Should return None for non-existent file"

def test_get_page_count_invalid_mime():
    # Test with unsupported mime type
    pdf_path = "data/vielse/manually_extracted/Bekendtgørelse af lov om ægteskabs indgåelse og opløsning.pdf"
    result = get_page_count(pdf_path, "invalid/mime")
    assert result is None, "Should return None for unsupported mime type"