# Functionality written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import sqlite3
from datetime import datetime
import os
from ..utils.mime_type import get_mime_type
from ..utils.doc_io import get_page_count, calculate_file_hash

class MetricsDatabaseConnection:
    def __init__(self, db_path: str = "processing_metrics/document_processing.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = None

    def __enter__(self) -> "MetricsDatabaseConnection":
        """Initialize SQLite database with required table."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                       CREATE TABLE IF NOT EXISTS processing_metrics
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           timestamp DATETIME,
                           ingest_method TEXT,
                           file_path TEXT,
                           file_size INTEGER,
                           file_hash TEXT,
                           mime_type TEXT,
                           page_count INTEGER,
                           processing_time REAL
                       )
                       ''')
        self.conn.commit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def save_metrics(
            self,
            ingestion_method: str,
            file_path: str,
            processing_time: float
    ):
        """Save processing metrics to database."""
        file_size = os.path.getsize(file_path)
        timestamp = datetime.now().isoformat()
        file_hash = calculate_file_hash(file_path)

        mime_type = get_mime_type(file_path)
        page_count = get_page_count(file_path,mime_type)

        self.cursor.execute('''
                       INSERT INTO processing_metrics
                       (timestamp, ingest_method, file_path, file_size, file_hash, mime_type, page_count, processing_time)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (timestamp, ingestion_method, file_path, file_size, file_hash, mime_type, page_count, processing_time))
        self.conn.commit()
