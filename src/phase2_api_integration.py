import requests
import os
from dotenv import load_dotenv
import json

# Load API credentials from .env
load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

# Example: Fetch reviews for a sample app (Apple ID: 364709193 for Facebook)
URL = f"https://{API_HOST}/v1/app-store-api/reviews"

params = {
    "id": "364709193",   # App ID (replace with any valid iOS app ID)
    "sort": "mostRecent",
    "page": "1",
    "country": "us",
    "lang": "en"
}

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

def fetch_appstore_data():
    try:
        response = requests.get(URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Save raw response
        os.makedirs("data/raw", exist_ok=True)
        with open("data/raw/appstore_api.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ API data saved to data/raw/appstore_api.json")

    except Exception as e:
        print(f"❌ Error fetching API data: {e}")

if __name__ == "__main__":
    fetch_appstore_data()
