# FastAPI User Management API

This project implements a production-style backend API using FastAPI with PostgreSQL, Redis, and Elasticsearch.

---

## How to Start the Project

The project can be run in two ways: using Docker (recommended) or manually using a Python virtual environment.

### Option 1: Run Using Docker (Recommended)

Docker provides a reproducible environment and avoids local dependency issues.

```bash
# Build the Docker image
docker build -t fastapi-assignment .

# Run the container
docker run -p 8080:8000 fastapi-assignment
```

The API will be available at `http://localhost:8080`

### Option 2: Run Manually (Local Development)

**1. Create and activate virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Start FastAPI server**

```bash
uvicorn api.main:app --reload --port 8001
```

The API will be available at `http://127.0.0.1:8001/status`

---

## Module 1: FastAPI Backend – User Management API

### Overview

This module implements a production-style backend API using FastAPI. It demonstrates proper backend architecture by combining:

- **PostgreSQL** as the source of truth
- **Redis** for caching read operations
- **Elasticsearch** for indexing/searching user data

The focus is on clean structure, correct data flow, and fault-tolerant design.

### Tech Stack

- Python
- FastAPI
- PostgreSQL – persistent storage
- Redis – caching layer
- Elasticsearch – indexing/search
- Docker – containerized runtime

---

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /status`

**Response:**

```json
{
  "status": "running",
  "timestamp": "UTC timestamp"
}
```

**Purpose:**

- Verify the API is running
- Used for monitoring and debugging

---

### 2. Create User

**Endpoint:** `POST /users/`

**Request Body:**

```json
{
  "name": "John",
  "email": "john@example.com",
  "role": "admin"
}
```

**Flow:**

1. Request is validated using Pydantic
2. User is stored in PostgreSQL (source of truth)
3. User data is indexed in Elasticsearch (best-effort)
4. Success response is returned

**Notes:**

- Duplicate users are rejected with `409 Conflict`
- Elasticsearch failures do not block user creation

---

### 3. Fetch User by Email

**Endpoint:** `GET /users/{email}`

**Flow:**

1. Check Redis cache
2. If cache miss → fetch from PostgreSQL
3. Store result in Redis with TTL
4. Return user details

**Notes:**

- Redis is used only for read optimization
- Cache failures do not break the API

---

## Architecture & Data Flow

### Write Path (User Creation)

```
Client → FastAPI → PostgreSQL → Elasticsearch
```

- PostgreSQL is the source of truth
- Elasticsearch is used only for indexing/search
- Redis is not involved in writes

### Read Path (Fetch User)

```
Client → Redis → PostgreSQL → Redis
```

- Redis is populated on read, not on write
- Database is always authoritative

---

## Key Design Principles

- **Source of Truth:** PostgreSQL holds all persistent data
- **Caching Strategy:** Redis caches reads with TTL-based expiration
- **Search Optimization:** Elasticsearch enables fast querying
- **Fault Tolerance:** Component failures don't cascade (graceful degradation)
- **Clean Architecture:** Separation of concerns between data persistence, caching, and search

---

## Module 2: Data Processing (ETL Simulation)

### Overview

This module demonstrates a simple ETL (Extract, Transform, Load) pipeline using Pandas. The goal is to process a sales dataset containing more than 5,000 records by cleaning the data and exporting it into optimized formats for further use.

### Dataset Description

- **Type:** Sales / E-commerce data
- **File:** `data/raw.csv`
- **Rows:** 5,000+
- **Columns include:**
  - `order_id`
  - `customer_id`
  - `product`
  - `quantity`
  - `price`
  - `order_date`

The dataset intentionally contains:

- Duplicate records
- Missing values
- Date values in string format

This simulates real-world raw data.

---

## ETL Steps

### 1. Extract

The raw CSV file is loaded using Pandas:

```python
pd.read_csv("data/raw.csv")
```

### 2. Transform

#### a. Remove Duplicates

Duplicate records are removed based on the business key `order_id`:

```python
df.drop_duplicates(subset=["order_id"])
```

**Reason:** Each order should be uniquely identified by `order_id`. Duplicate orders would cause incorrect sales reporting.

#### b. Handle Missing Values

Different strategies were applied based on column importance:

**Quantity**

Missing values are replaced with `1`:

```python
df["quantity"] = df["quantity"].fillna(1)
```

- Assumes minimum purchase quantity

**Order Date**

Rows with missing or invalid dates are dropped:

```python
df.dropna(subset=["order_date"])
```

**Reason:** Order date is critical for sales reporting and time-based analysis. Guessing or filling dates would introduce incorrect assumptions.

#### c. Convert Date Column

The `order_date` column is converted to a proper datetime format:

```python
pd.to_datetime(df["order_date"], errors="coerce")
```

Invalid dates are safely converted to `NaT` and removed.

### 3. Load

The cleaned dataset is exported into two formats:

- **CSV** – human-readable and widely compatible
- **Parquet** – columnar format optimized for analytics

```python
df.to_csv("data/processed_output.csv", index=False)
df.to_parquet("data/processed_output.parquet", index=False)
```

---

## Output Files

```
data/
├── raw.csv
├── processed_output.csv
└── processed_output.parquet
```

### Why Parquet?

Parquet is a columnar storage format that:

- Uses less disk space
- Provides faster read performance
- Is suitable for analytical workloads and large datasets

---

## How to Run Module 2

From the project root:

```bash
python etl.py
```

After execution, the processed files will be available in the `data/` directory.

**Note:** Module 2 outputs are automatically used by Module 3 for simulated S3 upload.

---

## Module 3: Data Serving & Storage Simulation (API + S3)

### Overview

This module extends the ETL pipeline by simulating how processed data is served and stored in a backend system. Instead of stopping at CSV/Parquet generation, the pipeline now mimics a real-world data flow where cleaned data is uploaded to object storage (S3-like).

The goal is to demonstrate:

- Understanding of post-ETL data handling
- Clean Python project structure
- Modular design and separation of concerns

---

## Project Structure

```
Python-Backend-Data-Engineering/
├── data/
│   ├── __init__.py
│   ├── etl.py
│   ├── raw.csv
│   ├── processed_output.csv
│   └── processed_output.parquet
├── s3_simulation.py
├── requirements.txt
└── README.md
```

---

## Module Responsibilities

### 1. ETL Execution (`data/etl.py`)

- Reads raw sales data (5K+ rows)
- Cleans and transforms the dataset
- Exports results into:
  - `processed_output.csv`
  - `processed_output.parquet`
- Triggers simulated upload to S3

### 2. S3 Upload Simulation (`s3_simulation.py`)

Since real AWS credentials are not used, this module simulates object storage behavior.

**Responsibilities:**

- Validate file existence
- Log upload actions
- Mimic production-style data persistence flow

**Example behavior:**

```
File processed_output.csv successfully uploaded to S3://test-bucket/processed_output.csv
```

---

## Why S3 Simulation?

In real data engineering systems:

- ETL jobs do not stop at file creation
- Processed data is pushed to:
  - S3
  - GCS
  - Azure Blob Storage

This simulation proves understanding of ETL → Storage flow without external dependencies.

---

## How to Run Module 3

**Step 1: Activate virtual environment**

```bash
source venv/bin/activate
```

**Step 2: Run ETL as a module (IMPORTANT)**

```bash
python -m data.etl
```

❗ **Important:** Running via `-m` ensures correct module resolution and clean imports.

---

## Expected Output

```
Initial rows: 5200
Rows after cleaning: 4680
ETL completed successfully
File processed_output.csv successfully uploaded to S3://test-bucket/processed_output.csv
File processed_output.parquet successfully uploaded to S3://test-bucket/processed_output.parquet
```

---

## Complete Workflow

```
Module 2 (ETL) → Module 3 (S3 Simulation)
```

1. **Module 2** processes raw data and generates:
   - `processed_output.csv`
   - `processed_output.parquet`

2. **Module 3** automatically uploads these files to simulated S3 storage

This demonstrates the complete data engineering pipeline from ingestion to storage.