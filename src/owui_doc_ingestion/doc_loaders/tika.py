import html2text
import requests
import logging
import sys
from enum import Enum
import re
from langchain_core.documents import Document

logging.basicConfig(stream=sys.stdout, level='DEBUG')
log = logging.getLogger(__name__)

class OutputFormat(str, Enum):
    TEXT = "text"
    HTML = "html"
    MD = "md"


# Copied from 
# https://github.com/open-webui/open-webui/blob/main/backend/open_webui/retrieval/loaders/main.py#L91
class TikaLoader:
    def __init__(
            self,
            url,
            file_path,
            mime_type=None,
            extract_images=None,
            # Extension compared to OWUI
            output_format: OutputFormat = OutputFormat.TEXT,
            html2md_engine="pandoc"
    ):
        self.url = url
        self.file_path = file_path
        self.mime_type = mime_type
        self.output_format = output_format
        self.html2md_engine = html2md_engine

        self.extract_images = extract_images

    def load(self) -> list[Document]:
        with open(self.file_path, "rb") as f:
            data = f.read()

        if self.mime_type is not None:
            headers = {"Content-Type": self.mime_type}
        else:
            headers = {}

        if self.extract_images == True:
            headers["X-Tika-PDFextractInlineImages"] = "true"

        endpoint = self.url
        if not endpoint.endswith("/"):
            endpoint += "/"

        endpoint += "tika"
        if self.output_format == OutputFormat.TEXT:
            endpoint += "/text"

        r = requests.put(endpoint, data=data, headers=headers)

        if r.ok & (self.output_format == OutputFormat.TEXT):
            raw_metadata = r.json()
            text = raw_metadata.get("X-TIKA:content", "<No text content found>").strip()

            if "Content-Type" in raw_metadata:
                headers["Content-Type"] = raw_metadata["Content-Type"]

            log.debug("Tika extracted text: %s", text)

            return [Document(page_content=text, metadata=headers)]
        elif r.ok:
            html_content = r.text
            # Extract Content-Type from meta tag
            content_type_match = re.search(r'<meta name="Content-Type" content="([^"]+)"', html_content)
            if content_type_match:
                headers["Content-Type"] = content_type_match.group(1)

            # Remove head section if present
            cleaned_html = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL)

            if self.output_format == OutputFormat.HTML:
                log.debug("Tika extracted html: %s", cleaned_html)
                return [Document(page_content=cleaned_html, metadata=headers)]
            if self.output_format == OutputFormat.MD:
                md_content = html2text.html2text(cleaned_html)
                log.debug("Tika extracted markdown: %s", md_content)
                return [Document(page_content=md_content, metadata=headers)]

            raise Exception(f"Error calling Tika: Unknown output format: {self.output_format}")
        else:
            raise Exception(f"Error calling Tika: {r.reason}")

