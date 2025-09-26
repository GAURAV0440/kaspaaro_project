import pandas as pd
import os

GOOGLE_CSV = "./data/processed/cleaned_apps.csv"
APPLE_CSV = "./data/processed/appstore_api_cleaned.csv"
OUTPUT_CSV = "./data/processed/combined_apps.csv"

def merge_datasets(google_path, apple_path, output_path):
    # Load Google Play data
    df_google = pd.read_csv(google_path)
    df_google = df_google.rename(columns={
        "App": "App_Name",
        "Rating": "Rating"
    })
    df_google["Platform"] = "GooglePlay"

    # Keep only relevant cols for Google
    google_cols = ["App_Name", "Category", "Rating", "Installs", "Size_MB", "Platform"]
    df_google = df_google[google_cols]

    # Load Apple App Store data
    df_apple = pd.read_csv(apple_path)
    df_apple = df_apple.rename(columns={
        "userName": "App_Name",
        "score": "Rating",
        "text": "Review_Text",
        "updated": "Last_Updated"
    })
    df_apple["Platform"] = "AppStore"

    # Keep only relevant cols for Apple
    apple_cols = ["App_Name", "Rating", "title", "Review_Text", "Last_Updated", "Platform"]
    df_apple = df_apple[apple_cols]

    # Merge datasets (stack)
    combined = pd.concat([df_google, df_apple], ignore_index=True, sort=False)

    # Save combined dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.to_csv(output_path, index=False)

    print(f"✅ Combined dataset saved to: {output_path}")

if __name__ == "__main__":
    merge_datasets(GOOGLE_CSV, APPLE_CSV, OUTPUT_CSV)
