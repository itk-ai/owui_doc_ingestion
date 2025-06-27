import os
import argparse
from urllib.parse import urlparse, quote
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from owui_doc_ingestion.doc_loaders.tika import TikaLoader

load_dotenv()

TIKA_SERVER_URL = os.getenv('TIKA_SERVER_URL')
TIKA_SERVER_USER = os.getenv('TIKA_SERVER_USER')
TIKA_SERVER_PWD = os.getenv('TIKA_SERVER_PWD')

PDF_EXTRACT_IMAGES = os.getenv('PDF_EXTRACT_IMAGES',False).lower() in ['true', '1', 't']

def set_url_username_password(url, username, password):
  _username = quote(username)
  _password = quote(password)
  _url = urlparse(url)
  _netloc = _url.netloc.split('@')[-1]
  _url = _url._replace(netloc=f'{_username}:{_password}@{_netloc}')
  return _url.geturl()

def main():
    parser = argparse.ArgumentParser(description="Process a list of file paths.")
    parser.add_argument('file_paths', nargs='+', help='List of paths to files')

    args = parser.parse_args()
    url = set_url_username_password(TIKA_SERVER_URL, TIKA_SERVER_USER, TIKA_SERVER_PWD)
    docs: List[Document] = []
    for file_path in args.file_paths:
        loader = TikaLoader(url, file_path, extract_images= PDF_EXTRACT_IMAGES)
        docs = docs + loader.load()


if __name__ == "__main__":
    main()