import pandas as pd
import json
import os

RAW_JSON = "./data/raw/appstore_api.json"
OUTPUT_CSV = "./data/processed/appstore_api_cleaned.csv"

def normalize_appstore_json(input_path, output_path):
    # Load raw JSON
    with open(input_path, "r") as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Keep only useful columns
    keep_cols = ["id", "userName", "version", "score", "title", "text", "updated"]
    df = df[keep_cols]

    # Convert updated column to datetime
    df["updated"] = pd.to_datetime(df["updated"], errors="coerce")

    # Save cleaned CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned App Store API data saved to: {output_path}")

if __name__ == "__main__":
    normalize_appstore_json(RAW_JSON, OUTPUT_CSV)
