import pandas as pd
import json
import os

# Define file paths for JSON to CSV conversion
RAW_JSON = "./data/raw/appstore_api.json"
OUTPUT_CSV = "./data/processed/appstore_api_cleaned.csv"

def normalize_appstore_json(input_path, output_path):
    # Load raw JSON data from API response
    # This is done because we need to process the JSON data from the API call
    with open(input_path, "r") as f:
        data = json.load(f)

    # Convert JSON data to pandas DataFrame for easier manipulation
    # I have used DataFrame because it provides better data processing capabilities
    df = pd.DataFrame(data)

    # Select only the columns we need for analysis
    # This is done because API returns many fields but we only need specific ones
    keep_cols = ["id", "userName", "version", "score", "title", "text", "updated"]
    df = df[keep_cols]

    # Convert date strings to proper datetime format
    # I have used this because proper dates enable time-based analysis
    df["updated"] = pd.to_datetime(df["updated"], errors="coerce")

    # Create output directory and save as CSV
    # This is done because the merger script expects CSV format input
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Cleaned App Store API data saved to: {output_path}")

if __name__ == "__main__":
    normalize_appstore_json(RAW_JSON, OUTPUT_CSV)
