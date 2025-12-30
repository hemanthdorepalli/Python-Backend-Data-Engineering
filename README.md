# How to Start the Project

This project can be run in two ways: using Docker (recommended) or manually using a Python virtual environment.

## Option 1: Run Using Docker (Recommended)

Docker provides a reproducible environment and avoids local dependency issues.

```bash
# Build the Docker image
docker build -t fastapi-assignment .

# Run the container
docker run -p 8080:8000 fastapi-assignment

## Option 2: Run Manually (Local Development)
1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Start FastAPI server
uvicorn api.main:app --reload --port 8001

http://127.0.0.1:8001/status