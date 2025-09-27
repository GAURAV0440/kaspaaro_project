import requests
import os
from dotenv import load_dotenv
import json

# Load API credentials from .env file
# This is done because API keys should never be hardcoded in source code for security
load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

# Configure API endpoint for fetching App Store reviews
# I have used Facebook app as an example (Apple ID: 364709193)
URL = f"https://{API_HOST}/v1/app-store-api/reviews"

# Set up API request parameters
# This is done because the API requires specific parameters to fetch relevant data
params = {
    "id": "364709193",   # App ID (replace with any valid iOS app ID)
    "sort": "mostRecent",
    "page": "1",
    "country": "us",
    "lang": "en"
}

# Configure request headers with authentication
# I have used these headers because the RapidAPI service requires authentication
headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

def fetch_appstore_data():
    try:
        # Make API request with timeout for reliability
        # I have used timeout to prevent the request from hanging indefinitely
        response = requests.get(URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Create directory if it doesn't exist
        # This is done because we need a place to store the raw API response
        os.makedirs("data/raw", exist_ok=True)
        
        # Save raw API response to file
        # I have used JSON format to preserve the original data structure
        with open("data/raw/appstore_api.json", "w") as f:
            json.dump(data, f, indent=2)

        print("SUCCESS: API data saved to data/raw/appstore_api.json")

    except Exception as e:
        print(f"ERROR: Failed to fetch API data: {e}")

if __name__ == "__main__":
    fetch_appstore_data()
