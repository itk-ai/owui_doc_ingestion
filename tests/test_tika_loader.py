# Test written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import pytest
import requests
import os
from owui_doc_ingestion.doc_loaders.tika import TikaLoader
from owui_doc_ingestion.utils.urls import set_url_username_password
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

def is_tika_server_available(url: str) -> bool:
    """Check if Tika server is available by calling its health check endpoint."""
    try:
        response = requests.get(f"{url}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


@pytest.fixture
def tika_url():
    """Fixture that provides the configured Tika URL and skips test if server is unavailable."""
    url = set_url_username_password(
        os.getenv('TIKA_SERVER_URL'),
        os.getenv('TIKA_SERVER_USER'),
        os.getenv('TIKA_SERVER_PWD')
    )
    if not is_tika_server_available(os.getenv('TIKA_SERVER_URL')):
        pytest.skip("Tika server is not available")
    return url


def test_tika_loader_document_extraction(tika_url):
    """Test actual document extraction with live Tika server."""
    # Arrange
    test_file_path = 'data/vielse/manually_extracted/Bekendtgørelse af lov om ægteskabs indgåelse og opløsning.pdf'
    extract_images = os.getenv('PDF_EXTRACT_IMAGES', 'false').lower() in ['true', '1', 't']

    # Act
    loader = TikaLoader(tika_url, test_file_path, extract_images=extract_images)
    docs = loader.load()

    # Assert
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert isinstance(docs[0], Document)
    assert len(docs[0].page_content) > 100
