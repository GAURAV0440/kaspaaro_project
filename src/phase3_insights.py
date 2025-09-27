import pandas as pd
import json
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables for API configuration
# This is done because API keys should never be hardcoded in source code
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini AI with API key
# I have used Gemini because it provides powerful AI insights for market analysis
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-pro-latest")

# Define file paths for data input and output
# I have used these paths to organize processed data and generated insights
INPUT_FILE = "./data/processed/combined_apps.csv"
OUTPUT_JSON = "./data/processed/insights.json"
OUTPUT_MD = "./reports/insights_report.md"

def generate_insights():
    # Load the combined cross-platform dataset
    # This is done because we need the processed data for analysis
    df = pd.read_csv(INPUT_FILE)

    # Calculate basic statistics for context
    # I have used these metrics to provide concrete data points for AI analysis
    avg_google_rating = df["Google_Rating"].mean(skipna=True)
    avg_apple_rating = df["Apple_Rating"].mean(skipna=True)
    total_apps = len(df)
    cross_platform_apps = df["Available_On_Both_Stores"].sum()

    # Create prompt for AI analysis
    # This is done because the AI needs specific context and instructions for quality insights
    prompt = f"""
    You are analyzing a cross-platform dataset of {total_apps} apps with {cross_platform_apps} available on both stores.
    Avg Google Play rating = {avg_google_rating:.2f}, Avg App Store rating = {avg_apple_rating:.2f}.
    
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

    # Generate AI insights using Gemini
    # This is done because we need intelligent analysis beyond basic statistics
    response = model.generate_content(prompt)
    
    # Clean the AI response to handle markdown formatting
    # I have used this because AI sometimes returns JSON wrapped in markdown code blocks
    response_text = response.text.strip()
    
    # Remove markdown code block markers if present
    # This is done because JSON parsing fails if markdown formatting is included
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    elif response_text.startswith("```"):
        response_text = response_text[3:]
    
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    
    response_text = response_text.strip()

    # Parse AI response as JSON with error handling
    # I have used try-catch because AI responses can sometimes be malformed
    try:
        insights = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"WARNING: JSON parse error: {e}")
        print(f"Raw response: {response.text[:200]}...")
        # Fallback to raw text if JSON parsing fails
        insights = {"raw_output": response.text}

    # Create output directories if they don't exist
    # This is done because we need folders to exist before saving files
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    
    # Save insights as JSON file for programmatic access
    # I have used JSON format because it's easy to parse in other applications
    with open(OUTPUT_JSON, "w") as f:
        json.dump(insights, f, indent=2)

    # Save insights as Markdown report for human readability  
    # I have used Markdown because it's readable and can be converted to other formats
    with open(OUTPUT_MD, "w") as f:
        f.write("# AI-Powered Market Insights\\n\\n")
        if isinstance(insights, list):
            for item in insights:
                f.write(f"- **Insight**: {item['insight']}\\n")
                f.write(f"  - Confidence: {item['confidence']}\\n\\n")
        else:
            f.write(str(insights.get('raw_output', 'No insights generated')))

    print(f"SUCCESS: Insights saved to {OUTPUT_JSON} and {OUTPUT_MD}")

if __name__ == "__main__":
    # Execute insight generation when script is run directly
    # This is done because we want the script to be executable from command line
    generate_insights()