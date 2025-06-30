import os
import argparse
import time
from dotenv import load_dotenv
from owui_doc_ingestion.doc_loaders.tika import TikaLoader
from owui_doc_ingestion.utils.urls import set_url_username_password
from owui_doc_ingestion.utils.doc_io import save_docs_to_md
from owui_doc_ingestion.processing_metrics.db import MetricsDatabaseConnection

load_dotenv()

TIKA_SERVER_URL = os.getenv('TIKA_SERVER_URL')
TIKA_SERVER_USER = os.getenv('TIKA_SERVER_USER')
TIKA_SERVER_PWD = os.getenv('TIKA_SERVER_PWD')

PDF_EXTRACT_IMAGES = os.getenv('PDF_EXTRACT_IMAGES',False).lower() in ['true', '1', 't']

def main():
    parser = argparse.ArgumentParser(description="Process a list of file paths.")
    parser.add_argument('file_paths', nargs='+', help='List of paths to files')
    parser.add_argument("--out_folder", help="Output folder for extracted text, default is same folder as input file",
                        default=None)

    args = parser.parse_args()
    url = set_url_username_password(TIKA_SERVER_URL, TIKA_SERVER_USER, TIKA_SERVER_PWD)
    with MetricsDatabaseConnection() as conn:
        for file_path in args.file_paths:
            loader = TikaLoader(url, file_path, extract_images= PDF_EXTRACT_IMAGES)
            start_time = time.time()
            docs = loader.load()
            processing_time = time.time() - start_time
            conn.save_metrics('tika', file_path, processing_time)

            save_docs_to_md(docs, file_path, args.out_folder)


if __name__ == "__main__":
    main()