import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables from .env file
# This is done because file paths should be configurable via environment variables
load_dotenv()

# Get file paths from environment variables with fallback defaults
# I have used environment variables to make the code flexible for different environments
RAW_PATH = os.getenv("DATA_RAW_PATH", "./data/raw/googleplaystore.csv")
PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH", "./data/processed/cleaned_apps.csv")

def clean_google_play_data(input_path: str, output_path: str):
    # Load the raw dataset from CSV file
    # This is done because we need to read the original Google Play data
    df = pd.read_csv(input_path)

    # Remove duplicate rows from dataset
    # This is done because duplicate apps can skew analysis results
    df.drop_duplicates(inplace=True)

    # Remove rows with missing essential information
    # I have used this because apps without name, category, or rating are not useful for analysis
    df.dropna(subset=["App", "Category", "Rating"], inplace=True)

    # Clean the Installs column by removing symbols and converting to numbers
    # This is done because install counts contain '+' and ',' symbols that prevent numeric operations
    if "Installs" in df.columns:
        df["Installs"] = (
            df["Installs"]
            .astype(str)
            .str.replace(r"[+,]", "", regex=True)
            .replace("Free", np.nan)
            .astype(float)
        )

    # Convert app sizes to standardized MB format
    # I have used this function because sizes are in different units (K, M) and need standardization
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

    # Apply size conversion to create standardized Size_MB column
    # This is done because we need consistent size measurements for comparison
    if "Size" in df.columns:
        df["Size_MB"] = df["Size"].apply(size_to_mb)

    # Convert ratings to numeric format for mathematical operations
    # I have used this because some ratings might be stored as strings
    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    # Reset row index numbers after cleaning operations
    # This is done because dropping rows creates gaps in index numbers
    df.reset_index(drop=True, inplace=True)

    # Create output directory and save the cleaned dataset
    # I have used this to ensure the output folder exists before saving
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Cleaned dataset saved to: {output_path}")

if __name__ == "__main__":
    # Execute the cleaning process when script is run directly
    # This is done because we want the script to be executable from command line
    clean_google_play_data(RAW_PATH, PROCESSED_PATH)
