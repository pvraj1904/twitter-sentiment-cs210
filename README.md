# Twitter Sentiment Analysis Dashboard (CS210 Project)

## Overview
A real-time Twitter sentiment analysis system that combines historical and live tweet data, processes it with NLP (VADER), and visualizes trends, top words, and more in an interactive Streamlit dashboard.

## Features
- Collects tweets via Kaggle dataset and X (Twitter) API
- Cleans, analyzes, and aggregates sentiment data
- Interactive dashboard (Streamlit) with charts, word clouds, user stats, filters

## Usage
1. Clone the repo
2. Set up your `.env` file (see `README` for variables)
3. Run each stage:
   - `python src/collect.py` / `collect_v2.py`
   - `python src/clean.py`
   - `python src/analyze.py`
   - `python src/aggregate.py`
   - `streamlit run src/dashboard.py`
4. See the dashboard at `http://localhost:8501`

## Authors
- Vraj Patel
- Vraj Soni
- Anurag Vattipalli

---
*For academic use (CS210 Summer 2025).*
