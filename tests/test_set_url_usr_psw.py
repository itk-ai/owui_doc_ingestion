# Test written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import pytest
from owui_doc_ingestion.utils.urls import set_url_username_password
from urllib.parse import quote

def test_set_url_username_password():
    # Test basic URL with simple credentials
    url = "http://example.com"
    username = "user"
    password = "pass"
    result = set_url_username_password(url, username, password)
    assert result == "http://user:pass@example.com"

    # Test URL with special characters that need encoding
    url = "https://example.com"
    username = "user@domain"
    password = "pass#word!"
    result = set_url_username_password(url, username, password)
    assert result == f"https://{quote('user@domain')}:{quote('pass#word!')}@example.com"

    # Test URL that already has credentials (should replace them)
    url = "http://olduser:oldpass@example.com"
    username = "newuser"
    password = "newpass"
    result = set_url_username_password(url, username, password)
    assert result == "http://newuser:newpass@example.com"

    # Test URL with port number
    url = "http://example.com:8080"
    username = "user"
    password = "pass"
    result = set_url_username_password(url, username, password)
    assert result == "http://user:pass@example.com:8080"

    # Test URL with path and query parameters
    url = "http://example.com/path?param=value"
    username = "user"
    password = "pass"
    result = set_url_username_password(url, username, password)
    assert result == "http://user:pass@example.com/path?param=value"
