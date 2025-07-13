from src.collect import collect_historical, collect_stream
from src.clean import clean_tweets
from src.analyze import analyze_sentiment
from src.aggregate import aggregate_data
import subprocess

def main():
    print("\n==== Step 1: Collecting historical tweets from Kaggle dataset ====")
    collect_historical()

    print("\n==== Step 2: (Optional) Collecting live tweets from Twitter API ====")
    collect_stream()

    print("\n==== Step 3: Cleaning and preprocessing tweets ====")
    clean_tweets()

    print("\n==== Step 4: Running sentiment analysis ====")
    analyze_sentiment()

    print("\n==== Step 5: Aggregating data for dashboard ====")
    aggregate_data()

    print("\n==== Step 6: Launching dashboard ====")
    subprocess.run(["streamlit", "run", "src/dashboard.py"])

if __name__ == "__main__":
    main()
