"""S3/MinIO client stubs used across the pipeline."""
import os
import tempfile
from pathlib import Path


def get_presigned_put_url(file_name: str) -> str:
    endpoint = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    bucket = os.getenv("S3_BUCKET", "fire-media")
    return f"{endpoint}/{bucket}/{file_name}?presigned=true"


def download_to_tmp(s3_key: str) -> str:
    """Placeholder that simulates a download by creating an empty file."""
    tmpdir = tempfile.mkdtemp()
    local_path = Path(tmpdir) / Path(s3_key).name
    local_path.touch()
    return str(local_path)
