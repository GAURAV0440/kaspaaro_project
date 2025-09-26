import pandas as pd
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# File paths
RAW_FILE = "./data/raw/Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx"
OUTPUT_FILE = "./data/processed/d2c_cleaned.csv"
INSIGHTS_FILE = "./data/processed/d2c_insights.json"

def clean_d2c():
    # Load Excel
    df = pd.read_excel(RAW_FILE)

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Drop duplicates & fill nulls
    df = df.drop_duplicates()
    df = df.fillna(0)

    # ---- Calculate key metrics ----
    # CAC = spend / installs
    df["cac"] = df.apply(lambda x: x["spend_usd"] / x["installs"] if x["installs"] > 0 else 0, axis=1)

    # ROAS = revenue / spend
    df["roas"] = df.apply(lambda x: x["revenue_usd"] / x["spend_usd"] if x["spend_usd"] > 0 else 0, axis=1)

    # CTR = clicks / impressions
    df["ctr"] = df.apply(lambda x: x["clicks"] / x["impressions"] if x["impressions"] > 0 else 0, axis=1)

    # Retention = repeat_purchase / first_purchase
    df["retention_rate"] = df.apply(lambda x: x["repeat_purchase"] / x["first_purchase"] if x["first_purchase"] > 0 else 0, axis=1)

    # Save cleaned CSV
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ D2C cleaned dataset with metrics saved to: {OUTPUT_FILE}")

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

    print(f"✅ D2C insights saved to: {INSIGHTS_FILE}")

if __name__ == "__main__":
    df = clean_d2c()
    generate_insights(df)
