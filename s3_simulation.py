from pathlib import Path

def upload_to_s3(data_file: str) -> str:

    file_path = Path(data_file)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {data_file}")

    filename = file_path.name

    # Simulated upload (no real AWS interaction)
    return f"File {filename} successfully uploaded to S3://test-bucket/{filename}"
