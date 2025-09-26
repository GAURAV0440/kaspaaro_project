import pandas as pd
import json
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-pro-latest")

INPUT_FILE = "./data/processed/combined_apps.csv"
OUTPUT_JSON = "./data/processed/insights.json"
OUTPUT_MD = "./reports/insights_report.md"

def generate_insights():
    # Load combined dataset
    df = pd.read_csv(INPUT_FILE)

    # Basic stats
    avg_rating = df["Rating"].mean(skipna=True)
    total_apps = len(df)
    google_apps = len(df[df["Platform"] == "GooglePlay"])
    apple_apps = len(df[df["Platform"] == "AppStore"])

    # Prompt for Gemini
    prompt = f"""
    You are analyzing a combined dataset of {total_apps} apps 
    (Google Play: {google_apps}, App Store: {apple_apps}).
    Avg rating = {avg_rating:.2f}.
    
    Generate 3 market insights:
    - Trends
    - Competitor performance
    - Recommendations
    
    For each, assign confidence as High, Medium, or Low.
    Return valid JSON array with keys: insight, confidence.
    Example:
    [
      {{"insight": "Sample text", "confidence": "High"}},
      {{"insight": "Sample text 2", "confidence": "Medium"}}
    ]
    """

    response = model.generate_content(prompt)
    insights_text = response.text

    # Clean response (remove ```json ... ```)
    clean_text = re.sub(r"```json|```", "", insights_text).strip()

    # Parse JSON safely
    try:
        insights = json.loads(clean_text)
    except Exception:
        insights = {"raw_output": insights_text}

    # Save JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(insights, f, indent=2)

    # Save Markdown report
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w") as f:
        f.write("# AI-Powered Market Insights\n\n")
        if isinstance(insights, list):
            for item in insights:
                f.write(f"- **Insight**: {item['insight']}\n")
                f.write(f"  - Confidence: {item['confidence']}\n\n")
        else:
            f.write(insights_text)

    print(f"✅ Insights saved to {OUTPUT_JSON} and {OUTPUT_MD}")

if __name__ == "__main__":
    generate_insights()
