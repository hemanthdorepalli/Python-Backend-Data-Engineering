import pandas as pd
from pathlib import Path
from s3_simulation import upload_to_s3

def run_etl():
    BASE_DIR = Path(__file__).resolve().parent

    # -------- EXTRACT --------
    df = pd.read_csv(BASE_DIR / "raw.csv")
    print("Initial rows:", len(df))

    # -------- TRANSFORM --------
    df = df.drop_duplicates(subset=["order_id"])

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = df["quantity"].fillna(1)
    df = df.dropna(subset=["order_date"])

    print("Rows after cleaning:", len(df))

    # -------- LOAD --------
    csv_path = BASE_DIR / "processed_output.csv"
    parquet_path = BASE_DIR / "processed_output.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    print("ETL completed successfully")

    # -------- SIMULATED S3 UPLOAD --------
    print(upload_to_s3(csv_path))
    print(upload_to_s3(parquet_path))


if __name__ == "__main__":
    run_etl()
