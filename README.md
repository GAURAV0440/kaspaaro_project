# AI-Powered Market Intelligence Dashboard

## Setup Instructions

### 1. Environment Configuration
1. Copy `.env.example` to `.env`
2. Add your actual API keys:
   - Get RapidAPI key from: https://rapidapi.com/
   - Get Gemini API key from: https://ai.google.dev/

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Usage
```bash
# Phase 1: Data Cleaning
python src/phase1_cleaning.py

# Phase 2: Data Integration
python src/phase2_api_integration.py

# Phase 3: Generate Insights
python src/phase3_insights.py

# Phase 4: Launch Dashboard
streamlit run src/phase4_dashboard.py
```

## Security Notice
⚠️ **Never commit API keys to version control!**
- Use `.env` file for local development
- Use environment variables in production
- Keep `.env` in `.gitignore`