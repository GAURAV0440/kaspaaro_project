import pandas as pd
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Define file paths for D2C analysis pipeline
# I have used these constants to make file locations easy to manage
RAW_FILE = "./data/raw/Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx"
OUTPUT_FILE = "./data/processed/d2c_cleaned.csv"
INSIGHTS_FILE = "./data/processed/d2c_insights.json"

def clean_d2c():
    # Load Excel file containing D2C marketing data
    # This is done because the raw data is stored in Excel format
    df = pd.read_excel(RAW_FILE)

    # Standardize column names to lowercase with underscores
    # I have used this because consistent naming makes data processing easier
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Remove duplicate records and fill missing values with zeros
    # This is done because duplicates skew analysis and nulls break calculations
    df = df.drop_duplicates()
    df = df.fillna(0)

    # Calculate key marketing performance metrics
    # I have used these calculations because they are essential for D2C analysis
    
    # CAC (Customer Acquisition Cost) = spend / installs
    # This is done because CAC is a critical metric for marketing efficiency
    df["cac"] = df.apply(lambda x: x["spend_usd"] / x["installs"] if x["installs"] > 0 else 0, axis=1)

    # ROAS (Return on Ad Spend) = revenue / spend
    # I have used this because ROAS measures marketing profitability
    df["roas"] = df.apply(lambda x: x["revenue_usd"] / x["spend_usd"] if x["spend_usd"] > 0 else 0, axis=1)

    # CTR = clicks / impressions
    df["ctr"] = df.apply(lambda x: x["clicks"] / x["impressions"] if x["impressions"] > 0 else 0, axis=1)

    # Retention = repeat_purchase / first_purchase
    df["retention_rate"] = df.apply(lambda x: x["repeat_purchase"] / x["first_purchase"] if x["first_purchase"] > 0 else 0, axis=1)

    # Save cleaned CSV
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"SUCCESS: D2C cleaned dataset with metrics saved to: {OUTPUT_FILE}")

    return df

def generate_insights(df):
    # Load API key
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-pro-latest")

    # Basic averages
    avg_cac = df["cac"].mean()
    avg_roas = df["roas"].mean()
    avg_conv = df["conversion_rate"].mean() * 100
    avg_ctr = df["ctr"].mean() * 100
    avg_ret = df["retention_rate"].mean() * 100

    prompt = f"""
    You are analyzing a synthetic D2C marketing dataset.
    Key averages:
    - CAC = ${avg_cac:.2f}
    - ROAS = {avg_roas:.2f}x
    - Conversion Rate = {avg_conv:.2f}%
    - CTR = {avg_ctr:.2f}%
    - Retention Rate = {avg_ret:.2f}%

    Generate:
    1. 3 key market insights (with confidence High/Medium/Low).
    2. 3 ad headlines (short, catchy).
    3. 3 SEO meta descriptions.
    4. 3 short product descriptions.
    
    IMPORTANT: Return ONLY valid JSON without any markdown formatting or code blocks.
    Example format:
    {{
        "insights": [
            {{"insight": "text", "confidence": "High"}},
            {{"insight": "text", "confidence": "Medium"}},
            {{"insight": "text", "confidence": "Low"}}
        ],
        "ad_headlines": ["headline1", "headline2", "headline3"],
        "seo_descriptions": ["desc1", "desc2", "desc3"],
        "product_descriptions": ["prod1", "prod2", "prod3"]
    }}
    """

    response = model.generate_content(prompt)
    
    # Clean the response text to handle markdown code blocks
    response_text = response.text.strip()
    
    # Remove markdown code block markers if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Remove "```json"
    elif response_text.startswith("```"):
        response_text = response_text[3:]   # Remove "```"
    
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Remove closing "```"
    
    # Clean any remaining whitespace
    response_text = response_text.strip()

    try:
        insights = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parse error: {e}")
        print(f"Raw response: {response.text[:200]}...")
        insights = {"raw_output": response.text}

    # Save insights
    os.makedirs(os.path.dirname(INSIGHTS_FILE), exist_ok=True)
    with open(INSIGHTS_FILE, "w") as f:
        json.dump(insights, f, indent=2)

    print(f"SUCCESS: D2C insights saved to: {INSIGHTS_FILE}")

if __name__ == "__main__":
    df = clean_d2c()
    generate_insights(df)
