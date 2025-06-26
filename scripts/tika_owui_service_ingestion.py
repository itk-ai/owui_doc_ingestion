import requests
from owui_doc_ingestion.doc_loaders.tika import TikaLoader


def main():
    loader = TikaLoader(
