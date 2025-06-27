# module written in colab with pycharm AI assistent (using Claude 3.5 Sonnet)
import magic
# NB on debian: apt install libmagic1
# on windows maybe consider mimetypes for guessing from extensions

def get_mime_type(file_path):
    """Determine MIME type using multiple methods."""
    try:
        # Use python-magic to get MIME type from file content
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type
    except Exception as e:
        print(f"Error detecting MIME type for {file_path}: {str(e)}")
        # Fallback to file extension
        if file_path.lower().endswith('.pdf'):
            return 'application/pdf'
        elif file_path.lower().endswith('.docx'):
            return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_path.lower().endswith('.doc'):
            return 'application/msword'
        return None
