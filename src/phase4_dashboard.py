import streamlit as st
import pandas as pd
import json
import os

# Define file paths for dashboard data sources
# I have used these constants to make file locations easy to maintain
COMBINED_CSV = "./data/processed/combined_apps.csv"
INSIGHTS_JSON = "./data/processed/insights.json"
REPORT_MD = "./reports/insights_report.md"
REPORT_HTML = "./reports/insights_report.html"

D2C_CSV = "./data/processed/d2c_cleaned.csv"
D2C_JSON = "./data/processed/d2c_insights.json"

# --- Data Loading Functions ---
@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

# Configure Streamlit page settings
# This is done because we want a professional-looking dashboard with proper title and layout
st.set_page_config(page_title="AI-Powered Market Intelligence", layout="wide")
st.title("AI-Powered Market Intelligence Dashboard")

tab1, tab2, tab3 = st.tabs(["📂 Dataset Overview", "🤖 Insights", "🛒 D2C Analysis"])

# =============== TAB 1: COMBINED DATASET ==================
with tab1:
    st.subheader("Cross-Platform Apps Dataset")
    df = load_csv(COMBINED_CSV)
    if not df.empty:
        st.dataframe(df.head(20))
        st.metric("Total Apps", len(df))
        st.metric("Cross-Platform Apps", df["Available_On_Both_Stores"].sum())
        st.metric("Avg Google Rating", f"{df['Google_Rating'].mean():.2f}")
        st.metric("Avg Apple Rating", f"{df['Apple_Rating'].mean():.2f}")

        # Download button
        st.download_button(
            "Download Cross-Platform Dataset (CSV)",
            data=df.to_csv(index=False),
            file_name="combined_apps.csv",
            mime="text/csv"
        )
    else:
        st.warning("No cross-platform dataset found. Run Phase 2 first.")

# =============== TAB 2: AI INSIGHTS ==================
with tab2:
    st.subheader("AI Insights")
    insights = load_json(INSIGHTS_JSON)

    if isinstance(insights, dict) and "raw_output" in insights:
        st.json(insights["raw_output"])
    elif isinstance(insights, list):
        for item in insights:
            st.markdown(f"**Insight:** {item['insight']}")
            st.markdown(f"🔒 Confidence: **{item['confidence']}**")
            st.markdown("---")
    else:
        st.warning("⚠️ No insights found. Run Phase 3 first.")

    # --- Download Reports ---
    if os.path.exists(REPORT_MD):
        with open(REPORT_MD, "r") as f:
            md_content = f.read()

        # Ensure HTML version exists
        with open(REPORT_HTML, "w") as f:
            f.write(f"<html><body><pre>{md_content}</pre></body></html>")

        st.download_button(
            "⬇️ Download Insights Report (Markdown)",
            data=md_content,
            file_name="insights_report.md"
        )
        st.download_button(
            "⬇️ Download Insights Report (HTML)",
            data=open(REPORT_HTML, "r").read(),
            file_name="insights_report.html",
            mime="text/html"
        )

# =============== TAB 3: D2C ANALYSIS ==================
with tab3:
    st.subheader("🛒 Kasparro D2C Analysis")

    d2c_df = load_csv(D2C_CSV)

    if not d2c_df.empty:
        st.write("### Dataset Preview")
        st.dataframe(d2c_df.head(15))

        # Key metrics
        st.write("### Funnel Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg CAC", f"${d2c_df['cac'].mean():.2f}")
        col2.metric("Avg ROAS", f"{d2c_df['roas'].mean():.2f}x")
        col3.metric("Avg Conversion Rate", f"{d2c_df['conversion_rate'].mean()*100:.2f}%")

        # SEO Metrics
        col4, col5 = st.columns(2)
        col4.metric("Avg CTR", f"{d2c_df['ctr'].mean()*100:.2f}%")
        col5.metric("Avg Retention Rate", f"{d2c_df['retention_rate'].mean()*100:.2f}%")

        # AI Insights & Creatives
        st.write("### 🤖 AI-Powered Insights")
        d2c_insights = load_json(D2C_JSON)

        if isinstance(d2c_insights, dict) and "raw_output" in d2c_insights:
            st.json(d2c_insights["raw_output"])
        elif isinstance(d2c_insights, dict):
            for section, content in d2c_insights.items():
                st.markdown(f"#### {section.capitalize()}")
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            st.markdown(f"- {item.get('insight', '')} ({item.get('confidence', '')})")
                        else:
                            st.markdown(f"- {item}")
                else:
                    st.write(content)
                st.markdown("---")

        # Download buttons
        st.download_button(
            "⬇️ Download D2C Cleaned Dataset (CSV)",
            data=d2c_df.to_csv(index=False),
            file_name="d2c_cleaned.csv",
            mime="text/csv"
        )
        st.download_button(
            "⬇️ Download D2C Insights (JSON)",
            data=json.dumps(d2c_insights, indent=2),
            file_name="d2c_insights.json",
            mime="application/json"
        )
    else:
        st.warning("⚠️ No D2C dataset found. Run Phase 5 first.")
