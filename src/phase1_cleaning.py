import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

RAW_PATH = os.getenv("DATA_RAW_PATH", "./data/raw/googleplaystore.csv")
PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH", "./data/processed/cleaned_apps.csv")

def clean_google_play_data(input_path: str, output_path: str):
    # Load dataset
    df = pd.read_csv(input_path)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Drop rows where essential columns are missing
    df.dropna(subset=["App", "Category", "Rating"], inplace=True)

    # Clean Installs column (remove + and , then convert to int)
    if "Installs" in df.columns:
        df["Installs"] = (
            df["Installs"]
            .astype(str)
            .str.replace(r"[+,]", "", regex=True)
            .replace("Free", np.nan)
            .astype(float)
        )

    # Clean Size column (convert K, M to numeric MB values)
    def size_to_mb(x):
        if isinstance(x, str):
            x = x.strip()
            if x.endswith("M"):
                return float(x.replace("M", ""))
            elif x.endswith("k") or x.endswith("K"):
                return float(x.replace("k", "").replace("K", "")) / 1024
            elif x == "Varies with device":
                return np.nan
        return np.nan

    if "Size" in df.columns:
        df["Size_MB"] = df["Size"].apply(size_to_mb)

    # Ensure Rating is numeric
    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    # Reset index after cleaning
    df.reset_index(drop=True, inplace=True)

    # Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned dataset saved to: {output_path}")

if __name__ == "__main__":
    clean_google_play_data(RAW_PATH, PROCESSED_PATH)
