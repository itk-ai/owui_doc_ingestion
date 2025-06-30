import os
import argparse
import time
from dotenv import load_dotenv
from owui_doc_ingestion.doc_loaders.docling import DoclingLoader
from owui_doc_ingestion.utils.urls import set_url_username_password
from owui_doc_ingestion.utils.doc_io import save_docs_to_md
from owui_doc_ingestion.processing_metrics.db import MetricsDatabaseConnection

load_dotenv()

DOCLING_SERVER_URL = os.getenv('DOCLING_SERVER_URL')
DOCLING_SERVER_USER = os.getenv('DOCLING_SERVER_USER')
DOCLING_SERVER_PWD = os.getenv('DOCLING_SERVER_PWD')

DOCLING_PARAMS={
    "ocr_engine": os.getenv('DOCLING_OCR_ENGINE',),
    "ocr_lang": os.getenv('DOCLING_OCR_LANG',"en,fr,de,es"),
    "do_picture_description": os.getenv('DOCLING_DO_PICTURE_DESCRIPTION').lower() in ['true', '1', 't'],
    "picture_description_mode": os.getenv('DOCLING_PICTURE_DESCRIPTION_MODE',""),
    "picture_description_local": os.getenv('DOCLING_PICTURE_DESCRIPTION_LOCAL',{}),
    "picture_description_api": os.getenv('DOCLING_PICTURE_DESCRIPTION_API',{}),
}

def main():
    parser = argparse.ArgumentParser(description="Process a list of file paths.")
    parser.add_argument('file_paths', nargs='+', help='List of paths to files')
    parser.add_argument("--out_folder", help="Output folder for extracted text, default is same folder as input file", default=None)

    args = parser.parse_args()
    url = set_url_username_password(DOCLING_SERVER_URL, DOCLING_SERVER_USER, DOCLING_SERVER_PWD)
    with MetricsDatabaseConnection() as conn:
        for file_path in args.file_paths:
            loader = DoclingLoader(url, file_path, params=DOCLING_PARAMS)
            start_time = time.time()
            docs = loader.load()
            processing_time = time.time() - start_time
            conn.save_metrics('docling', file_path, processing_time)

            save_docs_to_md(docs, file_path, args.out_folder)


if __name__ == "__main__":
    main()