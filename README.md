# AI-Powered Market Intelligence Dashboard

## What We Built
• **Cross-platform app analysis** - Compare same apps on Google Play and App Store
• **AI insights** - Smart analysis using Google Gemini AI
• **Interactive dashboard** - View data and insights in web browser
• **D2C marketing analysis** - Analyze marketing campaigns and performance
• **Secure API handling** - All API keys stored safely

## Quick Start
1. Copy `.env.example` to `.env` and add your API keys
2. Install: `pip install -r requirements.txt`
3. Run pipeline:
   ```bash
   python src/phase1_cleaning.py
   python src/phase2_api_integration.py
   python src/phase2_normalize.py
   python src/phase2_merge.py
   python src/phase3_insights.py
   streamlit run src/phase4_dashboard.py
   ```

## Files
• `phase1_cleaning.py` - Clean Google Play data
• `phase2_*.py` - Get App Store data and merge with Google Play
• `phase3_insights.py` - Generate AI insights
• `phase4_dashboard.py` - Web dashboard
• `phase5_d2c_cleaning.py` - Marketing analysis