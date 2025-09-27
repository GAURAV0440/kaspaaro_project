# Kasparro Project – Applied AI Engineer Assignment

This project was built as part of the Applied AI Engineer Assignment.
It covers data cleaning, API integration, insights generation, and a Streamlit dashboard.

## Features

Phase 1 – Clean raw Google Play dataset.

Phase 2 – Integrate App Store API, normalize, and merge datasets.

Phase 3 – Generate AI-powered insights & reports using Gemini.

Phase 4 – Interactive Streamlit dashboard (datasets, insights, downloads).

Phase 5 – D2C dataset cleaning, funnel + SEO metrics, ad creatives, AI insights.

## Setup Instructions

## Clone repo

git clone link
cd kasparro_project

Create virtual environment
python3 -m venv .venv
source .venv/bin/activate


Install dependencies
pip install -r requirements.txt

Set up environment variables
Create a .env file:

DATA_RAW_PATH=./data/raw/googleplaystore.csv
DATA_PROCESSED_PATH=./data/processed/cleaned_apps.csv

RAPIDAPI_KEY=******************
RAPIDAPI_HOST=***********
GEMINI_API_KEY=your_api_key_here


## How to Run
Phase 1 – Cleaning
python src/phase1_cleaning.py

Phase 2 – API + Merge
python src/phase2_api_integration.py
python src/phase2_normalize.py
python src/phase2_merge.py

Phase 3 – Insights
python src/phase3_insights.py

Phase 4 – Dashboard
streamlit run src/phase4_dashboard.py

Phase 5 – D2C Analysis
python src/phase5_d2c_cleaning.py

For Streamlit
streamlit run src/phase4_dashboard.py

<img width="1837" height="1005" alt="image" src="https://github.com/user-attachments/assets/01b101d1-61f6-4ba9-a068-d31893968add" />

<img width="1837" height="1005" alt="image" src="https://github.com/user-attachments/assets/bf210c39-a6fa-433e-8d71-f3afb021f351" />

<img width="1837" height="1005" alt="image" src="https://github.com/user-attachments/assets/31969e4b-c4dd-45af-b3e2-de80692a6c39" />
